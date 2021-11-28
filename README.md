# zerostore

Password storage, without the storage.

## Goals

The goal of this project is to serve as a proof-of-concept for a zero-storage password management system. This means that all the information needed to generate a secure, unique, per-site password can be kept in a user's head. In this way, users can eliminate password reuse without having to memorize multiple passwords or synch password databases between devices. A user should be able to go on any device with this program and have access to all of their passwords without having to import any data.

## Design

Per-site passwords are generated based on an account ID and a master password. The account ID should be a unique identifier for each account. For example, a combination of username and the domain on which it is used.

1. A master key is derived using scrypt, with the master password as the password and a constant+user ID as the salt. This is intended to increase the difficulty of brute-force attacks by deliberately increasing memory usage and processing time. Ideally, a random salt would be used, but this would be incompatible with the zero-storage design goal. Instead, the user ID is used as a salt which still prevents a pre-computed table of scrypt values being used across different users or domains.

2. The master key is used as the key for a SHA256-HMAC of the user ID. This ensures that generated passwords should have no detectable relationship with each other, and cannot be computed without knowing the master key.

3. The HMAC is then base64-encoded, truncated to given length, and used as the per-site password. This is designed to be compatible with as many sites' password requirements as possible. 
