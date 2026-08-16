import { describe, it, expect } from "vitest";
import {
  formatBytes,
  formatUptime,
  formatTimeRemaining,
  formatPercent,
  formatBitsPerSecond,
  formatFrequency,
  formatDurationShort,
} from "../src/lib/formatters";

describe("formatBytes", () => {
  it("returns 0 B for zero", () => {
    expect(formatBytes(0)).toBe("0 B");
  });

  it("formats KB", () => {
    expect(formatBytes(1024)).toBe("1.0 KB");
  });

  it("formats GB", () => {
    expect(formatBytes(2 * 1024 ** 3)).toBe("2.0 GB");
  });
});

describe("formatUptime", () => {
  it("shows minutes only", () => {
    expect(formatUptime(90)).toBe("1m");
  });

  it("shows hours and minutes", () => {
    expect(formatUptime(3661)).toBe("1h 1m");
  });

  it("shows days", () => {
    expect(formatUptime(90061)).toBe("1d 1h 1m");
  });
});

describe("formatTimeRemaining", () => {
  it("pads each component to two digits", () => {
    expect(formatTimeRemaining(3661)).toBe("01:01:01");
  });
});

describe("formatDurationShort", () => {
  it("formats seconds", () => {
    expect(formatDurationShort(45)).toBe("45s");
  });

  it("formats minutes", () => {
    expect(formatDurationShort(90)).toBe("1m");
  });

  it("formats hours only", () => {
    expect(formatDurationShort(7200)).toBe("2h");
  });

  it("formats hours and minutes", () => {
    expect(formatDurationShort(7260)).toBe("2h 1m");
  });
});

describe("formatPercent", () => {
  it("keeps one decimal", () => {
    expect(formatPercent(12.345)).toBe("12.3%");
  });
});

describe("formatBitsPerSecond", () => {
  it("formats bps", () => {
    expect(formatBitsPerSecond(100)).toBe("800 bps");
  });

  it("formats Mbps", () => {
    expect(formatBitsPerSecond(125000)).toBe("1.0 Mbps");
  });
});

describe("formatFrequency", () => {
  it("formats MHz", () => {
    expect(formatFrequency(800)).toBe("800 MHz");
  });

  it("formats GHz", () => {
    expect(formatFrequency(3200)).toBe("3.20 GHz");
  });
});
