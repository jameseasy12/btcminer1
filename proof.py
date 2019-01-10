"""
Hash Rate Proof Verification
Slush Pool <support@slushpool.com>

This is a public script to verify pool hash rate from a proof file.


Proof file is a zipped text file with line-based jsons (each line is one json). The first line is header - just key-value
json. Other lines are submits, one submit per line. We provide data to verify submit difficulty and our mark in
coinbase (/slush/). The file name (eg. 2016-02-01_16.zip) denotes the timestamp when the sampling period ends. This
proof file contains submits from 15:00 01/02/2016 to 16:00 01/02/2016.

Validation has two main parts. The first one is validation of the hash origin and the second one is the target validation
(quality of the hash). Validation of origin checks if coinbase transaction input contains our mark (/slush/). This
coinbase transaction must be in the merkle root in the block header.

Target validation computes double hash of block header and checks if the hash target is lower than the hash rate proof
target (computed from hash rate proof difficulty).

Each submit is validated by both validations.

The Script has only one argument - the gzipped proof file - that it operates on. There is no need to explicitly unzip
the proof file. The script prints result status and hash rate counted from number of proof submits and the proof
difficulty. If everything is correct, status is OK otherwise the status is ERR. When the status is ERR, the script
prints a reason for the error.

Structure of Proof File
-----------------------

First line is header

    {
        'version': <int>,  # integer - version of the proof script
        'difficulty': <int>,  # integer - network difficulty
    }

Other lines are submits

    [
        <str>,  # string (hex encoded) - block header
        <str>,  # string (hex encoded) - coinbase (with our sign /slush/)
        [<str>, ...],  # list of strings (hex encoded) - merkle branch of transactions to verify if our coinbase is in
                       # the block header
    ]
"""

import argparse
import binascii
import hashlib
import json
import os
from StringIO import StringIO
from zipfile import ZipFile


def hex_to_bin(data):
    return binascii.unhexlify(data)


def bin_to_hex(data):
    return binascii.hexlify(data)


def double_sha256_hash(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def bin_le_to_int(val):
    val_hex = bin_to_hex(val[::-1])
    return int(val_hex, 16)


def sha256_digest_to_int(data):
    return bin_le_to_int(data)


def difficulty_to_target(difficulty):
    BASE_DIFF_TARGET = 0x00000000ffff0000000000000000000000000000000000000000000000000000
    return int(BASE_DIFF_TARGET / difficulty)


def validate(hash_hex, difficulty):
    """
    Compute double hash of block header and check if the target is lower then the hash rate proof target (computed from
    hash rate proof difficulty).
    """
    return sha256_digest_to_int(double_sha256_hash(hex_to_bin(hash_hex))) < difficulty_to_target(difficulty)


def hashrate_from_proof(num_hashes, difficulty):
    """
    Count hash rate from numbers of hashes and hash rate proof difficulty (all submits above this difficulty are
    provided). Hash Rate is in the Gh/s
    """
    return (2**32 * difficulty * num_hashes)/float(3600 * 10**9)


def _format_unit_4sig(unit, value):
    if value >= 100:
        return u'%.1f %s' % (value, unit)
    if value >= 10:
        return u'%.2f %s' % (value, unit)
    return u'%.3f %s' % (value, unit)


def hashrate(variable):
    """
    Return hash rate in pretty format.
    """
    variable = float(variable)
    if abs(variable) < 0.0005:
        return '---'
    if variable < 1000:
        return _format_unit_4sig(u'Gh/s', variable)
    if variable < 1000000:
        return _format_unit_4sig(u'Th/s', variable / 1000.)

    return _format_unit_4sig(u'Ph/s', variable / 1000000.)


def compute_merkle_root(branch, first):
    """
    Compute merkle root from merkle branch and coinbase (first).
    """

    for s in branch:
        first = double_sha256_hash(first + s)
    return first


def validate_origin(hash_hex, coinbase_hex, merkle_branch_hex):
    """
    Validate if coinbase contains our mark (/slush/) and if merkle root and if the block header contains this merkle
    root.
    """

    hash_bin = hex_to_bin(hash_hex)
    coinbase_bin = hex_to_bin(coinbase_hex)
    merkle_branch_bin = map(hex_to_bin, merkle_branch_hex)
    merkle_root_bin = compute_merkle_root(merkle_branch_bin, double_sha256_hash(coinbase_bin))
    is_valid = True
    if '/slush/' not in coinbase_bin:
        print "Invalid coinbase, doesn't cointain '/slush/'"
        is_valid = False
    if merkle_root_bin != hash_bin[36:68]:
        print 'Invalid merkle root'
        is_valid = False
    return is_valid


def main(file_path):
    invalid = 0
    with ZipFile(file_path) as z:
        file_name = (os.path.basename(file_path).rsplit('.', 1)[0])+'.txt'
        f = StringIO(z.read(file_name))
        header = json.loads(f.readline())
        i = 0
        for line in f.readlines():
            hash, coinbase, merkle_branch = json.loads(line.replace('\n', ''))
            if not validate_origin(hash, coinbase, merkle_branch):
                invalid += 1
                i += 1
                continue
                return {
                    'status': 'ERR',
                    'err': 'wrong origin (missing /slush/ in coinbase or wrong merkle root)',
                    'hashrate': None,
                }
            if not validate(hash, header['difficulty']):
                return {
                    'status': 'ERR',
                    'err': 'too low difficulty',
                    'hashrate': None,
                }
            i += 1
    if invalid:
        return {
            'status': 'ERR',
            'err': 'wrong origin (missing /slush/ in coinbase or wrong merkle root) %d / %d' % (invalid, i),
            'hashrate': None,
        }

    return {
        'status': 'OK',
        'err': None,
        'hashrate': hashrate_from_proof(i, header['difficulty'])
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)

    args = parser.parse_args()

    res = main(args.file)
    print 'status:', res['status']
    if res['err']:
        print 'error:', res['err']
    print 'hashrate:', hashrate(res['hashrate'])
