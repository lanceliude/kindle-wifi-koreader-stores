# kTerm virtual keyboard character guide

Use this reference when guiding a non-technical user through the kTerm on-screen keyboard. Keep the Kindle command as short as possible.

## Recommended final command

Use exactly this shape, replacing IP and port:

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

Do not use variables, parentheses, semicolons or fallback chains on the Kindle side. The longer command caused shell continuation prompts during real testing.

## Character by character

- `wget` = lowercase letters.
- Space = tap `SPACE`.
- `-` = top number row.
- `q` = lowercase.
- `O` = uppercase letter O: tap Shift, then tap `o`.
- `-` = top number row.
- `http://` = lowercase `h t t p`, colon, two slashes.
- `:` = Shift + `;`.
- `/` = bottom letter row, directly available.
- IP address = digits and dots.
- Port = digits.
- `/g` = slash + lowercase `g`.
- `|` = pipe: Shift + `\`.
- `sh` = lowercase letters.

## Common mistakes

- `-qO-` uses the capital letter `O`, not the digit `0`.
- Do not type parentheses.
- Do not type `$u=...`.
- Do not add `|| curl ...` to the Kindle command.
- If a standalone `>` appears on the next line, the shell thinks the command is unfinished. Press Ctrl+C and retype the shorter command.

## kTerm keyboard layout hints

- Ctrl key is at the bottom-left.
- Shift is usually the upward-arrow / house-shaped key above `a`.
- Return/Enter is the arrow icon on the right of the third letter row.
- Semicolon `;` is on the third letter row after `l`.
- Backslash `\` is on the second letter row near `p`.
