#!/usr/bin/env python3
"""
示例：自动把 public-read S3 桶改成 private 并关掉 ACL
"""
import boto3, argparse, sys

def fix_public_buckets(dry_run=False):
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    for b in response["Buckets"]:
        name = b["Name"]
        acl = s3.get_bucket_acl(Bucket=name)
        grants = acl["Grants"]
        if any(g["Grantee"].get("URI", "").endswith("AllUsers") for g in grants):
            print(f"[!] Bucket {name} is PUBLIC")
            if dry_run:
                print("    (dry-run) would set ACL to private")
            else:
                s3.put_bucket_acl(Bucket=name, ACL="private")
                print("    -> ACL set to private ✔")
                
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="模拟运行，不真正修改")
    args = p.parse_args()
    fix_public_buckets(dry_run=args.dry_run)
