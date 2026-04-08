const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

describe('Python Automation Scripts - E2E Integration Tests', () => {
  let tmpDir;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pyauto-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  describe('file_organizer.py', () => {
    it('sorts files into subdirectories by extension', () => {
      fs.writeFileSync(path.join(tmpDir, 'report.pdf'), 'pdf content');
      fs.writeFileSync(path.join(tmpDir, 'photo.jpg'), 'jpg content');
      fs.writeFileSync(path.join(tmpDir, 'data.csv'), 'csv content');

      execSync(`python scripts/file_organizer.py "${tmpDir}"`, { cwd: process.cwd() });

      expect(fs.existsSync(path.join(tmpDir, 'pdf', 'report.pdf'))).toBe(true);
      expect(fs.existsSync(path.join(tmpDir, 'images', 'photo.jpg'))).toBe(true);
      expect(fs.existsSync(path.join(tmpDir, 'csv', 'data.csv'))).toBe(true);
    });

    it('skips directories and hidden files', () => {
      fs.mkdirSync(path.join(tmpDir, 'subdir'));
      fs.writeFileSync(path.join(tmpDir, '.hidden'), 'hidden');
      fs.writeFileSync(path.join(tmpDir, 'readme.txt'), 'text');

      execSync(`python scripts/file_organizer.py "${tmpDir}"`, { cwd: process.cwd() });

      expect(fs.existsSync(path.join(tmpDir, 'subdir'))).toBe(true);
      expect(fs.existsSync(path.join(tmpDir, '.hidden'))).toBe(true);
    });
  });

  describe('csv_report.py', () => {
    it('generates a summary report from input CSV', () => {
      const csvContent = 'name,amount,category\nAlice,100,food\nBob,200,transport\nAlice,50,food\n';
      const inputPath = path.join(tmpDir, 'input.csv');
      const outputPath = path.join(tmpDir, 'report.json');
      fs.writeFileSync(inputPath, csvContent);

      execSync(`python scripts/csv_report.py "${inputPath}" --output "${outputPath}"`, { cwd: process.cwd() });

      const report = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
      expect(report.total_rows).toBe(3);
      expect(report.total_amount).toBe(350);
      expect(report.by_category.food).toBe(150);
    });
  });

  describe('backup_script.py', () => {
    it('creates a timestamped zip archive of the source directory', () => {
      fs.writeFileSync(path.join(tmpDir, 'file1.txt'), 'content1');
      fs.writeFileSync(path.join(tmpDir, 'file2.txt'), 'content2');
      const backupDir = path.join(tmpDir, 'backups');
      fs.mkdirSync(backupDir);

      execSync(`python scripts/backup_script.py "${tmpDir}" --dest "${backupDir}"`, { cwd: process.cwd() });

      const archives = fs.readdirSync(backupDir).filter(f => f.endsWith('.zip'));
      expect(archives.length).toBe(1);
      expect(archives[0]).toMatch(/^backup_\d{8}_\d{6}\.zip$/);
    });
  });

  describe('log_analyzer.py', () => {
    it('parses log file and extracts error summary', () => {
      const logContent = [
        '2025-01-01 10:00:00 INFO Starting service',
        '2025-01-01 10:01:00 ERROR Connection timeout',
        '2025-01-01 10:02:00 WARNING Disk space low',
        '2025-01-01 10:03:00 ERROR Connection timeout',
        '2025-01-01 10:04:00 ERROR File not found',
      ].join('\n');
      const logPath = path.join(tmpDir, 'app.log');
      fs.writeFileSync(logPath, logContent);

      const output = execSync(`python scripts/log_analyzer.py "${logPath}"`, { cwd: process.cwd() }).toString();
      const result = JSON.parse(output);

      expect(result.total_lines).toBe(5);
      expect(result.errors).toBe(3);
      expect(result.top_errors[0].message).toBe('Connection timeout');
      expect(result.top_errors[0].count).toBe(2);
    });
  });
});
