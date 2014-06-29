eps = 0.0001;

function setupGrid(paper) {

    var Corner = function(x, y) {
        this.circle = paper.circle(x, y, 10);
        this.circle.attr("fill", "#f00");
        this.circle.attr("stroke", "#fff");

        // This is kept in sync with the centre when the point is not being
        // dragged.
        this.x = x;
        this.y = y;
        var corner = this;

        // Keep track of the distance moved since the start of the drag.
        // dx, dy are always relative to the start point, not the last move
        // event.
        var moved_x = 0;
        var moved_y = 0;
        var handleMove = function(dx, dy) {
            newdx = dx - moved_x;
            newdy = dy - moved_y;
            this.attr('cx', this.attr('cx') + newdx);
            this.attr('cy', this.attr('cy') + newdy);
            moved_x = dx;
            moved_y = dy;
        };
        var handleStart = function () {};
        var handleEnd = function() {
            moved_x = 0;
            moved_y = 0;
            corner.x = this.attr('cx');
            corner.y = this.attr('cy');
        };
        this.circle.drag(handleMove, handleStart, handleEnd);
    };

    var topleft = new Corner(50, 50);
    var bottomleft = new Corner(50, 200);
    var topright = new Corner(200, 50);
    var bottomright = new Corner(200, 200);

    var Grid = function (tl, tr, bl, br) {
        var grid = this;
        this.vp1 = paper.circle(300, 300, 5);
        this.tl = tl;
        this.tr = tr;
        this.bl = bl;
        this.br = br;
        var refresh = function() {
            grid.refresh();
        };
        this.br.circle.drag(function() {}, function() {}, refresh);

        // Create horizontal and vertical gridlines
        this.horizontal = [];
        this.vertical = [];
        var dy = ((bl.y - tl.y) / 18);
        var dx = ((tr.x - tl.x) / 18);
        for (var y = tl.y; y <= bl.y + eps; y += dy) {
            var path = 'M' + tl.x + ',' + y + 'L' + tr.x + ',' + y
            this.horizontal[this.horizontal.length] = paper.path(path);
        }
        for (var x = tl.x; x <= tr.x + eps; x += dx) {
            var path = 'M' + x + ',' + tl.y + 'L' + x + ',' + bl.y
            this.vertical[this.vertical.length] = paper.path(path);
        }
    }

    Grid.prototype.refresh = function() {
       var vertical_vanishing;

       var leftLine = getLineParams(this.tl.x, this.tl.y, this.bl.x, this.bl.y);
       var rightLine = getLineParams(this.tr.x, this.tr.y, this.br.x, this.br.y);

       if (leftLine === null && rightLine === null) {
           console.log('both vertical lines are actually vertical');
           vertical_vanishing === null;
       } else if (leftLine === null) {
           console.log('left is vertical');
           vertical_vanishing = getVerticalConvergence(this.tl.x, rightLine.m, rightLine.c);
       } else if (rightLine === null) {
           console.log('right is vertical');
           vertical_vanishing = getVerticalConvergence(this.tr.x, leftLine.m, leftLine.c);
       } else {
           vertical_vanishing = getConvergence(leftLine.m, leftLine.c, rightLine.m, rightLine.c);
       }

       if (vertical_vanishing === null) {
           console.log('both lines parallel');
       } else {
           console.log(vertical_vanishing);
       }
    };
    grid = new Grid(topleft, topright, bottomleft, bottomright);
};


/*
 * Get the convergence point of two lines, or null if they are parallel.
 */
function getConvergence(m1, c1, m2, c2) {
    if(Math.abs(m1 - m2) < eps) {
        return null;
    }

    result = {x: (c2 - c1) / (m1 - m2)};
    result.y = result.x * m1 + c1;
    return result;
}


/*
 * Get the convergence point of a vertical line with another line
 */
function getVerticalConvergence(x, m1, c1) {
    return m1 * x + c1;
}

/*
 * Draw a line between two points and return the equation
 * of the line.
 * Vertical lines return null.
 */
function getLineParams(x1, y1, x2, y2) {
    var dx = x1 - x2;
    if (Math.abs(dx) < eps) {
        return null;
    }
    m = (y1 - y2) / dx;
    c = y1 - m * x1;
    return {m: m, c: c}
}
