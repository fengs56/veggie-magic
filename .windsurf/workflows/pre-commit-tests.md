---
description: Run unit tests before committing changes
---

# Pre-Commit Test Workflow

This workflow runs comprehensive unit tests before you commit changes to ensure code quality and prevent regressions.

## Steps to Run Before Commit

1. **Run the unit test script**
   ```bash
   python test-veggie-magic.py
   ```

2. **Check test results**
   - ✅ If all tests pass: You can safely commit
   - ❌ If tests fail: Fix the issues before committing

3. **Start the development server** (optional, to manually verify)
   ```bash
   python -m http.server 8000
   ```

## What the Tests Cover

### Data Integrity Tests
- ✅ `meals.json` exists and is valid JSON
- ✅ Each meal has required fields (`name`, `miracleFruitCompatible`)
- ✅ Meal names are not empty strings
- ✅ Data types are correct (string for names, boolean for compatibility)

### Functionality Tests
- ✅ Miracle fruit filter logic works correctly
- ✅ Compatible meals contain expected sour keywords
- ✅ Filter counts add up correctly

### CSV Generation Tests
- ✅ CSV format is correct (headers, quoting)
- ✅ CSV can be parsed properly
- ✅ All meals are included in CSV output

### HTML Structure Tests
- ✅ `index.html` exists and contains required React components
- ✅ All UI elements are present (buttons, filter, etc.)
- ✅ Required functions are implemented

## Usage

### Quick Test Run
```bash
python test-veggie-magic.py
```

### Verbose Output
The script automatically runs with verbose output, showing:
- Individual test results
- Success/failure counts
- Clear pass/fail indication

### Integration with Git
You can integrate this with Git hooks by adding to `.git/hooks/pre-commit`:
```bash
#!/bin/sh
python test-veggie-magic.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Commit aborted."
    exit 1
fi
echo "✅ All tests passed. Proceeding with commit."
```

## Troubleshooting

### Common Issues
- **Python not found**: Make sure Python 3 is installed and in PATH
- **Missing meals.json**: Ensure the meals data file exists
- **Import errors**: Run from the project root directory

### Test Failures
- Check the specific test failure message
- Verify data structure in `meals.json`
- Ensure HTML file contains required components
- Check for typos in meal names or data fields

## Best Practices

1. **Run tests before every commit** - This ensures you don't break existing functionality
2. **Fix test failures immediately** - Don't commit with failing tests
3. **Add new tests for new features** - Keep the test suite comprehensive
4. **Update tests when changing data structure** - Maintain test relevance

## Test Coverage

The current test suite covers:
- Data validation (100% of meal data fields)
- Core functionality (filter logic, CSV generation)
- UI structure (required components and elements)
- Edge cases (empty names, invalid data)

This ensures your Veggie Magic app remains reliable and functional as you make changes.
