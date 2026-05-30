import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const pageRoot = resolve(here, '../src/pages');

function readPage(filename) {
  return readFileSync(resolve(pageRoot, filename), 'utf8');
}

function assertContains(source, expected) {
  assert.ok(
    source.includes(expected),
    `Expected fixture page source to contain ${JSON.stringify(expected)}`,
  );
}

test('LoginPage exposes stable login selectors', () => {
  const source = readPage('LoginPage.vue');

  assertContains(source, 'id="username"');
  assertContains(source, 'id="password"');
  assertContains(source, 'role="alert"');
  assertContains(source, 'data-testid="login-error"');
  assertContains(source, 'type="submit"');
});

test('UserDirectoryPage exposes stable search selectors', () => {
  const source = readPage('UserDirectoryPage.vue');

  assertContains(source, 'id="user-search-form"');
  assertContains(source, 'id="search-name"');
  assertContains(source, 'id="search-email"');
  assertContains(source, 'id="search-role"');
  assertContains(source, 'id="search-status"');
  assertContains(source, 'id="search-registered-from"');
  assertContains(source, 'id="search-registered-to"');
  assertContains(source, 'id="search-region"');
  assertContains(source, 'id="search-registered-range"');
  assertContains(source, 'id="search-month"');
  assertContains(source, 'id="btn-search"');
  assertContains(source, 'id="btn-reset"');
});

test('UserDirectoryPage exposes stable result selectors', () => {
  const source = readPage('UserDirectoryPage.vue');

  assertContains(source, 'data-user-id');
  assertContains(source, 'data-testid="user-detail"');
});

test('DashboardPage exposes stable dashboard selectors', () => {
  const source = readPage('DashboardPage.vue');

  assertContains(source, 'data-testid="dashboard-welcome"');
});
