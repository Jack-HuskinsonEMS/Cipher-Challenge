# National Cipher Challenge Workspace

This workspace contains custom tools for automating the decryption of classical ciphers.

## Ciphers We Can Solve

*   **Caesar Cipher** (`/Caesar/CaesarDecode.py`)
*   **Affine Cipher** (`/Affine`, `/Affine cypher/AD.py`, `/Affine cypher/BruteForce.py`)
*   **Monoalphabetic Substitution** (`/MonoSub/Ngram.py`)

## Ciphers We Cannot Solve Yet (Do Not Rebuild Existing Tools)

*   **Vigenère Cipher** (Polyalphabetic)
*   **Transposition Ciphers** (Rail Fence, Columnar)
*   **Hill Cipher**
*   **Playfair Cipher**

## Analysis Capabilities

*   **Index of Coincidence** (`/Affine cypher/IC.py`)
*   **Modular Multiplicative Inverse** (`/Affine cypher/ModularMultiplicativeInverse.py`)

## Competition Rules Reminder

*   **Do not use external code libraries** or black-box online solvers (like dCode or Boxentriq). All decryption code must be written by us.
*   **External data tables are completely allowed.** Using our offline `english_quadgrams.txt` or word lists to score text perfectly fits the rules.
*   **Submissions require no spaces.** The competition grading platform ignores spaces and punctuation entirely. Submit solutions as a solid uppercase string of letters.
