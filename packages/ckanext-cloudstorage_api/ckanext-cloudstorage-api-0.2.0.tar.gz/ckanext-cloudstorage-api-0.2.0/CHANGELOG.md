## 0.2.0 (2023-08-28)

### Feat

- remove IUploader, set url_type=s3, url in db
- add blueprint to download resources

### Fix

- remove redundant check_access in logic (in auth.py)
- update auth checks for each endpoint
- remove literal_eval for driver opts

### Refactor

- remove un-used util.py
- rename actions to original names (fast integration)
- rename clean_multiparts for clarity
- restructure ckan toolkit config imports

## 0.1.4 (2023-08-23)

### Fix

- inherit IResourceController methods to fix v2.10

## 0.1.3 (2023-08-23)

### Fix

- imports for multipart_check

## 0.1.2 (2023-08-23)

### Fix

- refactor storage.py, remove azure, simplify

## 0.1.1 (2023-08-22)

### Fix

- typos, rename cli to just cloudstorage

## 0.1.0 (2023-08-22)

### Feat

- first version of plugin

### Fix

- config for storage driver, v0.0.0
