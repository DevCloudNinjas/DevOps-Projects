export const PrintPlayerInMap = (player, map) => {
  var newMap = map.map(arr => arr.slice());
  for (let y = 0; y < player.bloco.bloco.length; y++)
    for (let x = 0; x < player.bloco.bloco.length; x++)
      if (player.bloco.bloco[y][x] === 1) {
        const pixelY = player.pos[0] + y;
        const pixelX = player.pos[1] + x;
        newMap[pixelY][pixelX] = { fill: 1, color: player.bloco.color };
      }
  return newMap;
};