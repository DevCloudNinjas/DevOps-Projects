const simpleTest = require('./simple.js').simpleTest;
const addTwo = require('./simple.js').addTwo;
const multTwo = require('./simple.js').multTwo;
const subTwo = require('./simple.js').subTwo;
const divTwo = require('./simple.js').divTwo;

describe('App', () => {
    test('simpleTest should return 1', () => {
        expect(simpleTest()).toBe(1);
    });
    test('addTwo should return 4', () => {
        expect(addTwo(2, 2)).toBe(4);
    });
    test('multTwo should return 6', () => {
        expect(multTwo(2, 3)).toBe(6);
    });
    test('subTwo should return 2', () => {
        expect(subTwo(4, 2)).toBe(2);
    });
    test('divTwo should return 2', () => {
        expect(divTwo(4, 2)).toBe(2);
    });
});