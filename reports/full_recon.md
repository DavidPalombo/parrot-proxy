# Parrot Proxy Report

Generated: 2026-05-29 02:41:29.358916+00:00

Campaign: full_recon

## Step: fuzz-params

Total Results: 8
Clusters: 8
Outlier Clusters: 8

| Payload | Status | Score |
|---|---|---|
| admin | 200 | 60 |
| root | 200 | 60 |
| ' OR 1=1 -- | 200 | 60 |
| <script>alert(1)</script> | 200 | 60 |
| admin | 200 | 60 |
| root | 200 | 60 |
| ' OR 1=1 -- | 200 | 60 |
| <script>alert(1)</script> | 200 | 60 |

## Step: fuzz-headers

Total Results: 4
Clusters: 0
Outlier Clusters: 0

| Payload | Status | Score |
|---|---|---|
| Authorization: admin | 200 | 0 |
| Authorization: root | 200 | 0 |
| Authorization: internal | 200 | 0 |
| Authorization: debug | 200 | 0 |

# Summary

High Value Findings: 8
