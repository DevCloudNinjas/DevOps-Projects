const calculator = require('./calculator')

test('string with a single number should result in the number itself', () => {
    expect(calculator.add('1')).toBe(1);
  });

  test('string with two numbers separated by comma should result in the sum of the numbers', () => {
    expect(calculator.add('4,5')).toBe(9);
  });

  test('string with three numbers separated by comma should result in the sum of the numbers', () => {
    expect(calculator.add('2,8,4')).toBe(14);
});

test('string with four numbers separated by comma should result in the sum of the numbers', () => {
    expect(calculator.add('2,0,4,5')).toBe(11);
});