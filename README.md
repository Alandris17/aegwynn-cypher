# The Song of Aegwynn Cipher

A Python implementation of a World of Warcraft-inspired substitution cipher based on a poetic key.
This project encodes and decodes messages using a dynamic Caesar-shift system derived from a reference poem.

---

## Concept

This cipher is inspired by a fictional encryption method where:

* A shared poem acts as the master key
* A reference number (formatted like a date) selects a starting word
* Each letter of that word determines a shift in the alphabet
* Punctuation changes the shift dynamically

---

## How It Works

### 1. Key Reference (Date Format)

The input format:

```
stanza.line.word
```

Example:

```
1.1.1
```

This means:

* Stanza 1
* Line 1
* Word 1

From *The Raven* by Edgar Allan Poe, this corresponds to:

> "Once upon a midnight dreary..."

So the key word is:

```
Once
```

---

### 2. Alphabet Shift

Each letter of the key word defines a shift:

| Letter | Shift |
| ------ | ----- |
| O      | 14    |
| n      | 13    |
| c      | 2     |
| e      | 4     |

* The first letter is used for the initial encoding
* After punctuation, the cipher moves to the next letter
* When the word ends, it loops back

---

### 3. Encoding Rule

Each character is shifted like a Caesar cipher:

```
new_letter = (original_letter + shift) % 26
```

* Uppercase and lowercase are preserved
* Non-alphabetic characters remain unchanged (except punctuation triggers)

---

### 4. Punctuation Behavior

Any punctuation mark (e.g. `. , ! ? : ;`) causes:

* The cipher to advance to the **next letter of the key word**

---

### 5. Numbers

Numbers are automatically converted into words before encoding:

```
2 -> "two"
```

---

## Usage

### Run the program

```
python main.py
```

### Example Input

```
Poem title: The Raven
Author: Edgar Allan Poe
Date: 1.1.1
Action: encode
Message: Hello World!
```

### Example Output

```
Encoded Message: Vszzc Kcfzr!
```

---

## Decoding

Use the same inputs and select `decode`:

```
Decoded Message: Hello World!
```

---

## Project Structure

```
.
├── main_fixed.py
├── The Raven - Edgar Allan Poe.txt
├── .gitignore
└── README.md
```

---

## Features

* Dynamic Caesar cipher based on literary key
* Bidirectional encoding/decoding
* Punctuation-driven shift changes
* Number-to-word conversion
* Flexible poem parsing (stanza/line/word)

---

## Limitations

* Requires correctly formatted poem files
* Key depends strictly on stanza/line/word structure
* Number conversion is basic (limited vocabulary)

---

## Inspiration

This project is inspired by a fictional encryption method from the Warcraft universe, specifically the lore surrounding the Order of Tirisfal in **World of Warcraft**.

In this setting, messages were encoded using a shared poetic key (*The Song of Aegwynn*), with references to stanza, line, and word acting as a starting point for the cipher.

This implementation recreates that concept as a functional cipher using real-world text (*The Raven* by Edgar Allan Poe) as the encryption key.

---
