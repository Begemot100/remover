import os
import sys
import hashlib
import pandas as pd


def get_hash(filename):
    block_size = 65536
    m = hashlib.sha256()

    try:
        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                m.update(block)
    except OSError:
        return 'Hash could not be generated.'

    return m.hexdigest()


def create_hashtable(folder):
    files = [entry.path for entry in os.scandir(folder) if entry.is_file()]
    print(f'[+] Found {len(files)} files in {folder}.')

    df = pd.DataFrame({'file': files})
    df['hash'] = df['file'].apply(get_hash)
    print('[+] Generated all hashes.')

    return df


def list_duplicates(folder):
    df = create_hashtable(folder)
    duplicates = df[df.duplicated(subset='hash', keep=False)].sort_values(by='hash')
    print(f'[+] Found {len(duplicates)} duplicates.\n')
    print(duplicates)

    return duplicates


if __name__ == '__main__':
    folder = input('Folder full path (e.g., C:/Users/bob/Desktop): ').strip()
    if not os.path.exists(folder):
        print('Folder does not exist.')
        sys.exit(1)

    duplicates = list_duplicates(folder)
    delete = input('\n[!] Do you want to delete the duplicates (y/n): ').strip().lower()
    print('\n')

    if delete == 'y':
        for file_path in duplicates['file']:
            os.remove(file_path)
            print(f'Deleted {file_path}')
    else:
        print('[X] Exiting...')
