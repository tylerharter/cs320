# Sample Hints

Here's a function that might be useful for pulling in on row at a time:

```python
import csv
from zipfile import ZipFile
from io import TextIOWrapper

def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row
```

If you are not faimilar with `yield` statement, it would be a good
idea to review generator from the lab.

Here's an example snippet that might use the above to print off IP addresses:

```python
reader = zip_csv_iter("large.zip")
header = next(reader) # the list of all column names
ip_idx = header.index("ip")
for row in reader:
    print(row[ip_idx])
```

Running the above will give output like this: (Note that it will be a large amount of print lines)

```
104.197.32.ihd
208.77.214.jeh
54.197.228.dbe
108.39.205.jga
52.45.218.ihf
104.197.32.ihd
183.195.251.hah
68.180.231.abf
107.178.195.bbb
107.3.20.gcd
...
```

Yes, those aren't quite real IP addresses, as explained in the next section...

Now, you will need to know how to write a zip file. For this, you can modify the following example, which make another zip2 file from the first five rows (+ the row of column names) of zip1 file.

```python
# save 5 rows of zip1 to zip2 
zip1 = "large.zip"
zip2 = "five_rows.zip"

reader = zip_csv_iter(zip1)
header = next(reader)

with ZipFile(zip2, "w") as zf:
    with zf.open(zip2.replace(".zip", ".csv"), "w") as raw:
        with TextIOWrapper(raw) as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header) # write the row of column names to zip2
            line_count = 0
            for row in reader:
                writer.writerow(row) # write a row to zip2
                line_count += 1
                if line_count == 5: # fifth row
                    break
```

After it, you will be able to check the `"five_rows.zip"` by the following codes.

```python
reader = zip_csv_iter(zip2)
header = next(reader)
ip_idx = header.index("ip")

for row in reader:
    print(row[ip_idx])
```

Expected result for the above code is:

```
104.197.32.ihd
208.77.214.jeh
54.197.228.dbe
108.39.205.jga
52.45.218.ihf
```
