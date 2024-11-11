document.querySelector('.menu-button').addEventListener('click', function() {
  // classList.toggle('active') 表示如果 .navbar 元素上有 active 类，则移除该类；如果没有 active 类，则添加该类
  document.querySelector('.navbar').classList.toggle('active');
});
