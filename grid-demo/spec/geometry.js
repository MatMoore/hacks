describe("A convergence point", function() {
    it("does not exist for parallel lines", function () {
        expect(getConvergence(1, 2, 1, 3)).toEqual(null);
    });

    it("calculation has a threshold to account for floating point errors", function() {
        expect(getConvergence(1, 2, 1.00005, 3)).toEqual(null);
    });

    it("lies on the origin when both C params are zero", function () {
        var point = getConvergence(1, 0, 2, 0);
        expect(Math.abs(point.x)).toEqual(0);
        expect(Math.abs(point.y)).toEqual(0);
    });
});
