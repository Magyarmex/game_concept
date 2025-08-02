const spriteFiles = ['frame1.txt', 'frame2.txt'];

export default await Promise.all(
  spriteFiles.map(name => fetch(`sprites/${name}`).then(res => res.text()))
);
