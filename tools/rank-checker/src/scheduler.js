/**
 * Scheduler for automated rank checking
 * Port of scheduler logic from AppGUI._run_scheduler_loop in v4.1.py
 *
 * Supports: run once, interval (minutes), daily at specific time
 */

class Scheduler {
    constructor() {
        this.running = false;
        this.mode = 'once';       // 'once' | 'interval' | 'daily'
        this.intervalMinutes = 60;
        this.dailyTime = '17:00';
        this.task = null;         // async function to run
        this.timer = null;
        this.currentRun = null;
    }

    /**
     * Start the scheduler
     * @param {Function} task - Async function to execute
     * @param {object} options - { mode, intervalMinutes, dailyTime }
     */
    start(task, options = {}) {
        if (this.running) {
            return { success: false, message: 'Scheduler already running' };
        }

        this.task = task;
        this.mode = options.mode || 'once';
        this.intervalMinutes = options.intervalMinutes || 60;
        this.dailyTime = options.dailyTime || '17:00';
        this.running = true;

        console.log(`[Scheduler] Started: mode=${this.mode}`);

        this._execute();

        return { success: true, message: `Scheduler started (${this.mode})` };
    }

    /**
     * Stop the scheduler
     */
    stop() {
        this.running = false;
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        console.log('[Scheduler] Stopped');
        return { success: true, message: 'Scheduler stopped' };
    }

    /**
     * Get scheduler status
     */
    getStatus() {
        return {
            running: this.running,
            mode: this.mode,
            intervalMinutes: this.intervalMinutes,
            dailyTime: this.dailyTime,
            nextRun: this._getNextRunTime(),
        };
    }

    /**
     * Internal: execute the scheduler loop
     */
    async _execute() {
        try {
            if (this.mode === 'once') {
                await this._runTask();
            } else if (this.mode === 'interval') {
                while (this.running) {
                    await this._runTask();
                    if (!this.running) break;
                    console.log(`[Scheduler] Next run in ${this.intervalMinutes} minutes`);
                    await this._sleep(this.intervalMinutes * 60 * 1000);
                }
            } else if (this.mode === 'daily') {
                while (this.running) {
                    await this._sleepUntil(this.dailyTime);
                    if (!this.running) break;
                    await this._runTask();
                }
            }
        } catch (err) {
            console.error('[Scheduler] Error:', err);
        } finally {
            this.running = false;
        }
    }

    async _runTask() {
        if (!this.task || !this.running) return;
        try {
            console.log('[Scheduler] Running task...');
            this.currentRun = this.task();
            await this.currentRun;
            console.log('[Scheduler] Task completed');
        } catch (err) {
            console.error('[Scheduler] Task error:', err);
        }
        this.currentRun = null;
    }

    _sleep(ms) {
        return new Promise(resolve => {
            this.timer = setTimeout(resolve, ms);
        });
    }

    async _sleepUntil(hhmm) {
        const [h, m] = hhmm.split(':').map(Number);
        const now = new Date();
        const target = new Date(now);
        target.setHours(h, m, 0, 0);
        if (target <= now) target.setDate(target.getDate() + 1);

        const waitMs = target.getTime() - Date.now();
        console.log(`[Scheduler] Waiting until ${hhmm} (${Math.round(waitMs / 60000)} minutes)`);
        await this._sleep(waitMs);
    }

    _getNextRunTime() {
        if (!this.running) return null;
        if (this.mode === 'daily') {
            const [h, m] = this.dailyTime.split(':').map(Number);
            const now = new Date();
            const target = new Date(now);
            target.setHours(h, m, 0, 0);
            if (target <= now) target.setDate(target.getDate() + 1);
            return target.toISOString();
        }
        return null;
    }
}

module.exports = new Scheduler();
