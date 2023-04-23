# Splendor

Splendor is a prototype tool for static discovery of stored XSS from PHP source code.
It now supports two scanning methods: If the complete database query string is available in the source code, Splendor will use string analysis for database read/write location analysis of the tainted data (Direct method[1]). Otherwise Splendor performs a DAL analysis and uses a fuzzy matching way to get this information(Fuzzy matching method).

## Basis of analysis
Our analysis is based on phpJoern[2].

[1] Dahse, Johannes and Thorsten Holz. “Static Detection of Second-Order Vulnerabilities in Web Applications.” USENIX Security Symposium (2014).<br>
[2] https://github.com/malteskoruppa/phpjoern
