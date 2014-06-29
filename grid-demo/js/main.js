eps = 0.0001;

function setupGrid(paper) {

    var Corner = function(x, y) {
        this.circle = paper.circle(x, y, 10);
        this.circle.attr("fill", "#f00");
        this.circle.attr("stroke", "#fff");

        // This is kept in cync with the centre when the point is not being
        // dragged.
        this.x = x;
        this.y = y;

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
            this.x = this.attr('cx');
            this.y = this.attr('cy');
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
        console.log('refresh');
        // Vanishing points for vertical lines
        // (vertical is defined in relation to the corners; these may be
        // moved around but we assume that opposite sides always stay opposite.)
        //
        // Step 1: are the left/right lines parallel?
        // Y = MX + C
        // (Y1 - Y2) / (X1 - X2) = M
        // Y1 - M X1 = C
        var left_dx = this.tl.x - this.bl.x;
        var right_dx = this.tr.x - this.br.x;
        left_m = (this.tl.y - this.bl.y) / left_dx;
        right_m = (this.tr.y - this.br.y) / right_dx;
        left_c = this.tl.y - left_m * this.tl.y;
        right_c = this.tr.y - left_m * this.tr.y;
        console.log(this.tl);
        console.log(this.tl.x);
        console.log(this.bl.x);
        if (left_dx == 0) {
            console.log('left is vertical');
            return;
        }
        if (right_dx == 0) {
            console.log('right is vertical');
            return;
        }
        if (Math.abs(left_m - right_m) < eps) {
            console.log('Parallel');
            // The lines are indeed parallel.
            // This means all the vertical grid lines will be parallel to each other,
            // and to the horizon (where horizontal lines meet).
            vertical_vanishing = null;
            return;
        } else {
            console.log('vertical lines angled');
            // The lines are not parallel. Find where they converge.
            // Y_l = Y_r
            //     = M_l X + C_l = M_r X + C_r
            // (M_l - M_r) X = C_r - C_l
            // X = (C_r - C_l) / (M_l - M_r)
            console.log(right_c, left_c, left_m, right_m);
            vertical_vanishing = {'x': (right_c - left_c) / (left_m - right_m)};
            vertical_vanishing.y = vertical_vanishing.x * left_m + left_c;
        }

        // Now horizontal lines
        //

        if (vertical_vanishing !== null) {
            console.log(vertical_vanishing.x, vertical_vanishing.y);
            this.vp1.transform("...t" + vertical_vanishing.x + "," + vertical_vanishing.x);
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

    // Y_l = Y_r
    //     = M_l X + C_l = M_r X + C_r
    // (M_l - M_r) X = C_r - C_l
    // X = (C_r - C_l) / (M_l - M_r)
    console.log(c2, c1, m1, m2);
    result = {'x': (c2 - c1) / (m1 - m2)};
    result.y = result.x * m1 + c1;
    return result;
}


/*
 * Get the convergence point of a vertical line with another line
 */
function getVerticalConvergence(x, m1, c1) {
}

/*
 * Draw a line between two points and return the equation
 * of the line.
 * Vertical lines return null.
 */
function getLineParams(x1, x2, y1, y2) {
}
