class std {
    constructor() {
        this.sum2_x = 0;
        this.sum_x = 0;
        this.N = 0;
    }

    step(x) {
        try {
            this.sum2_x = this.sum2_x + x * x;
            this.sum_x = this.sum_x + x;
            this.N = this.N + 1;
        } catch (e) {
            console.log('Exception in [' + arguments.callee.caller.name + '] function!');
        }
    }

    finalize() {
        try {
            let Ex2 = this.sum2_x / this.N;
            let E2x = (this.sum_x / this.N) * (this.sum_x / this.N);
            let s = (Ex2 - E2x);
            if (s < 0) {
                s = 0; // sometimes when Ex2 and E2x are very small, one can get a negative answer.
            }
            s = Math.pow(s, 0.5);
            return s;
        } catch (e) {
            console.log('Exception in [' + arguments.callee.caller.name + '] function!');
        }
    }
}