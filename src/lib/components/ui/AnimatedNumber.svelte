<script lang="ts">
  let { value = 0, duration = 400, decimals = 1, suffix = "", prefix = "" }: {
    value?: number;
    duration?: number;
    decimals?: number;
    suffix?: string;
    prefix?: string;
  } = $props();

  let displayed = $state(0);
  let raf: number | null = null;

  $effect(() => {
    const target = value;
    if (raf !== null) cancelAnimationFrame(raf);

    const start = displayed;
    const startTime = performance.now();
    const diff = target - start;

    if (Math.abs(diff) < 0.01) {
      displayed = target;
      return;
    }

    function step(now: number) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      displayed = start + diff * eased;

      if (progress < 1) {
        raf = requestAnimationFrame(step);
      } else {
        displayed = target;
        raf = null;
      }
    }

    raf = requestAnimationFrame(step);
  });
</script>

<span class="tabular-nums">{prefix}{displayed.toFixed(decimals)}{suffix}</span>
