const HUE_INIT = (11 * Math.PI) / 12;
const HUE_INCREMENT = Math.PI / 8;
const HUE_CUTOFF = 6;
const SAT = 0.7;
const VAL = 1;

const STEP_MODULUS = 4; // mouse move steps per update
const CELL_LENGTH = 3; // px
const canvas = document.getElementById("banner-animation");
const banner = document.getElementById("banner");
const ctx = canvas.getContext("2d");
const WHITE = "rgb(255, 255, 255)";

class GameOfLife {
  // FIXME - handle resize
  constructor() {
    this.setupGame();
    this.runRenderLoop();
    window.addEventListener("resize", () => this.setupGame());
    this.runGame();
  }

  setupGame() {
    // Set dimensions
    this.iters = 0;
    this.width = canvas.offsetWidth;
    this.height = canvas.offsetHeight;
    canvas.width = this.width;
    canvas.height = this.height;

    // Build grid
    this.numRows = Math.ceil(this.height / CELL_LENGTH);
    this.numCols = Math.ceil(this.width / CELL_LENGTH);
    this.grid = [];
    for (let i = 0; i < this.numRows; i++) {
      const row = [];
      this.grid.push(row);
      for (let j = 0; j < this.numCols; j++) {
        const val = Math.random() > 0.8 ? 1 : 0;
        row.push(val);
      }
    }
  }

  runRenderLoop() {
    this.renderGrid();
    requestAnimationFrame(() => this.runRenderLoop());
  }

  runGame() {
    for (let i = 0; i < 10; i++) {
      this.progressGame();
    }
    let counter = 0;
    window.addEventListener("mousemove", (e) => {
      if (counter % STEP_MODULUS == 0) {
        this.progressGame();
      }
      counter++;
    });
  }

  progressGame() {
    // Progress the game according to the GOL rules
    // Construct a new grid
    const nextGrid = Array(this.numRows)
      .fill(0)
      .map((row) => Array(this.numCols).fill(0));

    for (let rowIdx = 0; rowIdx < this.numRows; rowIdx++) {
      for (let colIdx = 0; colIdx < this.numCols; colIdx++) {
        nextGrid[rowIdx][colIdx] = this.grid[rowIdx][colIdx];
      }
    }

    // Fill grid
    for (let rowIdx = 0; rowIdx < this.numRows; rowIdx++) {
      for (let colIdx = 0; colIdx < this.numCols; colIdx++) {
        const numNeighbours = this.countNeighbours(rowIdx, colIdx);
        const cellValue = this.grid[rowIdx][colIdx];
        const liveCellSurvives =
          cellValue >= 1 && (numNeighbours === 2 || numNeighbours === 3);
        const deadCellLives = cellValue === 0 && numNeighbours === 3;
        if (deadCellLives) {
          nextGrid[rowIdx][colIdx] = 1;
        } else if (liveCellSurvives) {
          nextGrid[rowIdx][colIdx] += 1;
        } else {
          nextGrid[rowIdx][colIdx] = 0;
        }
      }
    }
    this.grid = nextGrid;
  }

  countNeighbours(rowIdx, colIdx) {
    // Counts the number of living neighbors for a cell
    let numNeighbours = 0;
    for (let i = -1; i < 2; i++) {
      for (let j = -1; j < 2; j++) {
        const isInBounds =
          rowIdx + i > -1 &&
          colIdx + j > -1 &&
          rowIdx + i < this.numRows &&
          colIdx + j < this.numCols &&
          !(i === 0 && j === 0);
        if (!isInBounds) continue;
        const neighbourAlive = this.grid[rowIdx + i][colIdx + j] > 0;
        if (neighbourAlive) {
          numNeighbours += 1;
        }
      }
    }
    return numNeighbours;
  }

  renderGrid() {
    // Render every grid element
    for (let rowIdx = 0; rowIdx < this.numRows; rowIdx++) {
      for (let colIdx = 0; colIdx < this.numCols; colIdx++) {
        const cellValue = this.grid[rowIdx][colIdx];
        if (cellValue > 0) {
          ctx.fillStyle = getFillStyle(cellValue);
        } else {
          ctx.fillStyle = WHITE;
        }

        ctx.fillRect(
          colIdx * CELL_LENGTH,
          rowIdx * CELL_LENGTH,
          CELL_LENGTH,
          CELL_LENGTH
        );
      }
    }
  }
}

const getFillStyle = (value) => {
  // Rotate initial hue by input angle (radians)
  const clippedValue = value > HUE_CUTOFF ? HUE_CUTOFF : value;
  const hue =
    (2 * Math.PI + HUE_INIT + clippedValue * HUE_INCREMENT) % (2 * Math.PI);
  // Converts HSV to RGB
  // #1 - calculate inscrutable intermediate values
  const h = hue / (Math.PI / 3);
  const c = VAL * SAT;
  const x = c * (1 - Math.abs((h % 2) - 1));
  const o = VAL - c;

  // #2 - smash them together
  const idx = Math.floor(h);
  const rgb = huePrimeLookup(x, c)
    [idx].map((color) => color + o)
    .map((color) => Math.round(255 * color));

  // Turn RGB to CSS string
  return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
};
huePrimeLookup = (x, c) => [
  [c, x, 0],
  [x, c, 0],
  [0, c, x],
  [0, x, c],
  [x, 0, c],
  [c, 0, x],
  [0, 0, 0],
];

new GameOfLife();
