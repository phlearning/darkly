# Darkly

> 🇫🇷 [Version française](README.fr.md) · 📖 [Glossary](GLOSSARY.md)

Web security project from the 42 curriculum. The goal is to audit a deliberately vulnerable website (the `Darkly` ISO, run in a VM), find **14 vulnerabilities**, exploit each one to retrieve a flag, and document the exploitation and the fix.

> ⚠️ **Spoiler warning:** each `Resources/*.md` write-up contains the flag and the full exploitation path.

## Setup

The target is a VirtualBox VM built from the official ISO (`Darkly_i386.iso`).

```bash
./vm.sh   # downloads the ISO, creates and configures the VM (port forwarding 4242)
```

The site is then reachable on the VM IP (or via port forwarding, e.g. `http://localhost:8080`).

## Repository layout

Each vulnerability has its own folder, named `<owasp-category>_<technique>`:

```
<owasp-category>_<technique>/
├── flag          # the flag obtained
└── Resources/    # write-up (.md), scripts, wordlists, payloads
```

## Vulnerabilities

| # | Folder | Technique | OWASP Top 10 (2021) |
|---|--------|-----------|---------------------|
| 1 | `broken-access-control_cookie-tampering` | Forge the `I_am_admin` cookie (weak MD5 hash of `false` replaced by the hash of `true`) | A01 Broken Access Control |
| 2 | `broken-access-control_directory-indexing-bruteforce` | Multi-threaded crawl of the `/.hidden/` tree (~18,000 README files) | A01 Broken Access Control |
| 3 | `broken-access-control_hidden-input-manipulation` | Edit a `hidden` input on the password recovery form | A01 Broken Access Control |
| 4 | `broken-access-control_lfi-directory-traversal` | `../` traversal in the `page` parameter to read `/etc/passwd` | A01 Broken Access Control |
| 5 | `broken-access-control_open-redirect` | Unvalidated `site` parameter in the redirect feature | A01 Broken Access Control |
| 6 | `broken-access-control_parameter-tampering-survey` | Send an out-of-range grade by editing the `<select>` value | A01 Broken Access Control |
| 7 | `broken-access-control_unrestricted-file-upload` | Upload a `.php` file disguised as `image/jpeg` | A01 / A04 |
| 8 | `identification-and-authentication-failures_brute-force` | Brute-force the `admin` login (GET form, no rate limiting) with a Python script | A07 Identification and Authentication Failures |
| 9 | `injection_reflected-xss-data-uri-bypass` | Reflected XSS through a `data:text/html;base64` URI to bypass the character filter | A03 Injection |
| 10 | `injection_sql-union-based` | Union-based SQL injection on the member page (quotes bypassed with hex) | A03 Injection |
| 11 | `injection_sql-union-search-image` | Union-based SQL injection on the image search, then MD5 decode and SHA-256 | A03 Injection |
| 12 | `injection_stored-xss-client-bypass` | Stored XSS split across two fields to bypass client-side `maxlength` | A03 Injection |
| 13 | `insecure-design_http-header-tampering` | Spoof `Referer` and `User-Agent` with `curl` | A04 Insecure Design |
| 14 | `security-misconfiguration_exposed-credentials` | Exposed `.htpasswd` in `/whatever/`, MD5 hash cracked, login on `/admin/` | A05 Security Misconfiguration |

## Tools used

`curl`, browser DevTools, `hashcat`, CrackStation, Python (`requests`, `ThreadPoolExecutor`), SecLists wordlists.

## Key takeaways

- Never trust client-side data (cookies, hidden fields, headers, `maxlength`, `<select>` values): **validate on the server**.
- Use whitelists for file paths, redirect targets and upload types.
- Use prepared statements and output encoding against injection.
- Do not rely on obscurity, and do not store secrets with fast, broken hashes like MD5.
- Add rate limiting and lockout on authentication endpoints.
