# Glossary

🇫🇷 [Version française](GLOSSARY.fr.md) · [Back to README](README.md)

| Term | Definition |
|------|------------|
| **Brute force** | Systematically trying many credentials or values until one works. |
| **Cookie tampering** | Modifying a cookie value client-side to change server behaviour. |
| **CrackStation / Rainbow table** | Precomputed hash-to-plaintext lookup used to reverse weak unsalted hashes. |
| **Data URI** | A `data:` URL embedding content directly (e.g. `data:text/html;base64,...`). |
| **Directory indexing** | A web server listing the contents of a directory. |
| **Directory traversal** | Using `../` sequences to escape the intended directory. |
| **Hidden input** | An `<input type="hidden">` field: invisible but fully editable by the client. |
| **`.htpasswd`** | Apache file storing user credentials for HTTP authentication. |
| **Insecure Design** | OWASP category: flaws in the design itself, not just the implementation. |
| **LFI (Local File Inclusion)** | Making the server include or read a local file chosen by the attacker. |
| **MD5** | Obsolete hash function, fast and collision-prone; unsuitable for passwords. |
| **Open redirect** | A redirect endpoint that accepts arbitrary destinations, useful for phishing. |
| **OWASP Top 10** | Reference list of the most critical web application security risks. |
| **Parameter tampering** | Altering request parameters beyond what the UI allows. |
| **Prepared statement** | Parameterised SQL query that separates code from data, preventing SQL injection. |
| **Rate limiting** | Restricting the number of requests a client can make in a given time. |
| **Referer / User-Agent** | HTTP request headers, set by the client and therefore forgeable. |
| **Reflected XSS** | Injected script returned immediately in the response to the same request. |
| **Security through obscurity** | Relying on secrecy of a location or design instead of real access control. |
| **SQL injection (SQLi)** | Injecting SQL fragments into a query through unsanitised input. |
| **Stored XSS** | Injected script saved by the server and served to later visitors. |
| **UNION-based SQLi** | SQLi using `UNION SELECT` to append attacker-chosen data to a query result. |
| **Unrestricted file upload** | Accepting uploaded files without properly validating type, extension or content. |
| **Whitelist** | Allow-list of accepted values; everything else is rejected. |
| **XSS (Cross-Site Scripting)** | Injecting JavaScript that runs in another user's browser. |
