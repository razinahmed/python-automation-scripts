const { execSync } = require('child_process');
const path = require('path');

function runPyTest(testModule) {
  return execSync(`python -m pytest tests/python/${testModule} -v --tb=short`, {
    cwd: process.cwd(),
    encoding: 'utf8',
  });
}

describe('Python Automation Scripts - Unit Tests (via pytest bridge)', () => {
  // These tests invoke Python pytest suites and check exit codes.
  // The actual assertions live in tests/python/*.

  describe('file_organizer module', () => {
    it('categorizes extensions correctly', () => {
      const result = execSync('python -c "from scripts.file_organizer import categorize_extension; assert categorize_extension(\'.jpg\') == \'images\'"', { encoding: 'utf8' });
      expect(result).toBeDefined();
    });

    it('maps pdf to pdf category', () => {
      const result = execSync('python -c "from scripts.file_organizer import categorize_extension; assert categorize_extension(\'.pdf\') == \'pdf\'"', { encoding: 'utf8' });
      expect(result).toBeDefined();
    });

    it('maps unknown extensions to misc', () => {
      const result = execSync('python -c "from scripts.file_organizer import categorize_extension; assert categorize_extension(\'.xyz\') == \'misc\'"', { encoding: 'utf8' });
      expect(result).toBeDefined();
    });
  });

  describe('csv_report module', () => {
    it('parses CSV rows into records', () => {
      const cmd = `python -c "
from scripts.csv_report import parse_csv_string
records = parse_csv_string('name,amount\\nAlice,100\\nBob,200')
assert len(records) == 2
assert records[0]['name'] == 'Alice'
assert int(records[0]['amount']) == 100
"`;
      execSync(cmd, { encoding: 'utf8' });
    });

    it('computes sum of a numeric column', () => {
      const cmd = `python -c "
from scripts.csv_report import sum_column
records = [{'amount': '10'}, {'amount': '20'}, {'amount': '30'}]
assert sum_column(records, 'amount') == 60
"`;
      execSync(cmd, { encoding: 'utf8' });
    });

    it('groups records by category', () => {
      const cmd = `python -c "
from scripts.csv_report import group_by
records = [{'cat': 'a', 'val': '1'}, {'cat': 'b', 'val': '2'}, {'cat': 'a', 'val': '3'}]
grouped = group_by(records, 'cat')
assert len(grouped['a']) == 2
assert len(grouped['b']) == 1
"`;
      execSync(cmd, { encoding: 'utf8' });
    });
  });

  describe('log_analyzer module', () => {
    it('extracts log level from standard log line', () => {
      const cmd = `python -c "
from scripts.log_analyzer import parse_log_line
result = parse_log_line('2025-01-01 10:00:00 ERROR Connection refused')
assert result['level'] == 'ERROR'
assert result['message'] == 'Connection refused'
"`;
      execSync(cmd, { encoding: 'utf8' });
    });

    it('returns None for malformed lines', () => {
      const cmd = `python -c "
from scripts.log_analyzer import parse_log_line
result = parse_log_line('this is not a log line')
assert result is None
"`;
      execSync(cmd, { encoding: 'utf8' });
    });

    it('counts error occurrences correctly', () => {
      const cmd = `python -c "
from scripts.log_analyzer import count_errors
lines = ['2025-01-01 ERROR Timeout', '2025-01-01 INFO Ok', '2025-01-01 ERROR Timeout', '2025-01-01 ERROR Disk full']
result = count_errors(lines)
assert result['Timeout'] == 2
assert result['Disk full'] == 1
"`;
      execSync(cmd, { encoding: 'utf8' });
    });
  });

  describe('backup_script module', () => {
    it('generates correct timestamped filename', () => {
      const cmd = `python -c "
from scripts.backup_script import generate_backup_name
import re
name = generate_backup_name()
assert re.match(r'backup_\d{8}_\d{6}\.zip', name)
"`;
      execSync(cmd, { encoding: 'utf8' });
    });

    it('filters out excluded patterns', () => {
      const cmd = `python -c "
from scripts.backup_script import should_include
assert should_include('data.txt') == True
assert should_include('.git') == False
assert should_include('__pycache__') == False
assert should_include('node_modules') == False
"`;
      execSync(cmd, { encoding: 'utf8' });
    });
  });
});
