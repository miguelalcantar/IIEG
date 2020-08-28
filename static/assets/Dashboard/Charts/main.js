const monthLabel = ['Enero','Febrero','Marzo','Abril','Mayo','Junio'];
// const monthLabel = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
const hourLabel = ['00:01 to 02:00', '02:01 to 04:00', '04:01 to 06:00', '06:01 to 08:00', '08:01 to 10:00', '10:01 to 12:00', '12:01 to 14:00', '14:01 to 16:00', '16:01 to 18:00', '18:01 to 20:00', '20:01 to 22:00', '22:01 to 24:00', 'N.D.'];
const ageLabel = ['10 A 19', '20 A 29', '30 A 39', '40 A 49', '50 A 59', '60 A 69', '70 Y MAS', 'N.D.'];

function line(labels, values, id, title){
  new Chart(document.getElementById(id),{
    "type":"line",
    "data":{
      "labels":labels,
      "datasets":[{
        "label":title,
        "data":values,
        "fill":false,
        "borderColor":"rgb(75, 192, 192)",
        "lineTension":0.1}]},
    "options":{}});
};

function bar(labels, values, id, title){
  new Chart(document.getElementById(id),{
    "type":"bar",
    "data":{
      "labels":labels,
      "datasets":[{
        "label":title,
        "data":values,
        "fill":false,
        "backgroundColor":generateColors(values.length),
        "lineTension":0.1}]},
    "options":{}});
};

function horizontalBar(labels, values, id, title){
  new Chart(document.getElementById(id),{
    "type":"horizontalBar",
    "data":{
      "labels":labels,
      "datasets":[{
        "label":title,
        "data":values,
        "fill":false,
        "backgroundColor":generateColors(values.length),
        "lineTension":0.1}]},
    "options":{}});
};

function pie(labels, values, id, title){
  new Chart(document.getElementById(id),{
    "type":"pie",
    "data":{
      "labels":labels,
      "datasets":[{
        "label":title,
        "data":values,
        "fill":false,
        "backgroundColor":generateColors(values.length)}]},
    "options":{}});
};

function generateColors(n){
  var arr = [];
  
  for(var i = 0; i < n; i ++){
    var number1 = Math.floor(Math.random() * 255).toString();
    var number2 = Math.floor(Math.random() * 255).toString();
    var number3 = Math.floor(Math.random() * 255).toString();
    arr.push("rgba(".concat(number1,", ",number2,", ",number3,", 0.3)"));
  };
  return arr;
};