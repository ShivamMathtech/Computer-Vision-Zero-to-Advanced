# Level 1 — Beginner

Use generated arrays, not downloaded photos. Write your own code before consulting the lesson again. For each answer, print shape/dtype and show a small plot when helpful.

1. **Build a flag.** Make a 6-row, 9-column RGB image with three vertical color stripes. Explain each slice. Check that the result has 162 channel values.
2. **Find a pixel.** In `tiny_palette()`, print the color at `(x=2, y=0)`. Then select only its blue value. Explain why the first index is not x.
3. **Count storage.** Calculate the byte count for a 10×20 RGB `uint8` image by hand, then compare with `.nbytes`. Repeat for `float32`.
4. **Write a function.** Return a new image with a chosen channel set to zero. Validate that the channel index is 0, 1 or 2, and prove the input was not changed.
5. **Use a dictionary.** Store brightness, three gains and a seed under meaningful keys. Apply the brightness setting to an image and print a short description.
6. **Plot responsibly.** Display a 3×3 grayscale array with intensity labels. Use fixed 0–255 limits. Explain what an automatic display scale could hide.
7. **Save and read.** Save your flag as PNG, reload it and check exact equality. Print the filename, shape and type without a machine-specific absolute path.

## Completion check

Can you explain a value without rerunning the cell? Your code should be readable to a classmate and run after restarting the notebook kernel.
