describe("a convergence point", function() {
    it("does not exist for parallel lines", function () {
        expect(getConvergence(1, 2, 1, 3)).toEqual(null);
    });

    it("calculation has a threshold to account for floating point errors", function() {
        expect(getConvergence(1, 2, 1.00005, 3)).toEqual(null);
    });

    it("lies on the origin when both C params are zero", function () {
        var point = getConvergence(1, 0, 2, 0);
        // Zero can be positive or negative. Thanks IEEE
        expect(Math.abs(point.x)).toEqual(0);
        expect(Math.abs(point.y)).toEqual(0);
    });

    it("can have positive x and y components", function () {
        var point = getConvergence(1, 1, 2, 0);
        expect(point.x).toEqual(1);
        expect(point.y).toEqual(2);
    });

    it("can have negative x and y components", function () {
        var point = getConvergence(2, 2, 1, 0);
        expect(point.x).toEqual(-2);
        expect(point.y).toEqual(-2);
    });

    it("can be determined from the c component if it's equal for both lines", function () {
        var point = getConvergence(123.456, -20, 3.14, -20);
        expect(Math.abs(point.y + 20)).toBeLessThan(0.0001);
        expect(Math.abs(point.x)).toBeLessThan(0.0001);
    });
});

describe("a vertical convegence point", function() {
    it("can be positive", function () {
        var point = getVerticalConvergence(10, 1, 0);
        expect(point).toEqual(10);
    });

    it("can be negative", function () {
        var point = getVerticalConvergence(10, -1, 0);
        expect(point).toEqual(-10);
    });

    it("lies on the vertical line if the other line is horizontal", function () {
        var point = getVerticalConvergence(22, 0, 123);
        expect(point).toEqual(123);
    });
});

describe("line parameters", function() {
    it("are not defined for a vertical line", function () {
        var line = getLineParams(1, 2, 1, 4);
        expect(line).toEqual(null);
    });

    it("has an intercept of zero if one of the points is the origin", function() {
        var line = getLineParams(0, 0, 1, 1);
        expect(line.c).toEqual(0);
    });

    it("has a positive slope if increasing x increases y", function() {
        var line = getLineParams(123, 456, 12, 13);
        expect(line.m).toBeGreaterThan(0);
    });

    it("has a negative slope if increasing x decreases y", function() {
        var line = getLineParams(123, 56, 12, 213);
        expect(line.m).toBeLessThan(0);
    });
});

describe("a parallel line", function() {
    it("goes through the provided point", function () {
        var point = {x: 1, y: 1};
        var line = {m: 1, c: 1};
        var result = getParallelLine(line, point);
        expect(result.c).toEqual(0);
    });

    it("shares the gradient of the original line", function () {
        var point = {x: 1, y: 1};
        var line = {m: 1, c: 1};
        var result = getParallelLine(line, point);
        expect(result.m).toEqual(1);
    });
});
