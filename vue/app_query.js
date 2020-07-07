var vm = new Vue({
  el: '#app',
  data: {
    map: null,
    tileLayer: null,
    pic: null,
    updated_pic: null,
    results: [],
    imageSelected: false,
    fps: [],
    car_color: null,
    car_size: null,
  },
  mounted() {
    this.showImage();
  },
  methods: {
    showImage() {
      // console.log(camid);
      var req = "http://127.0.0.1:5000/image?all=0";

      axios.get(req).then(response => {
          this.results = response.data;
          console.log(response.data);
      })


    },
    process(fp){
      // for (object in this.results) {
      //   console.log("in loop");
      // }
      // console.log("process_fps
      // this.results.forEach((item, i) => {
      //   this.fps.push("../keras-yolo3/static/"+item.filepath);
      // });
      var new_fp = "../keras-yolo3/static/images/"+fp;
      console.log(new_fp);
      return new_fp;

    },
    changeColor(color) {
      this.car_color = color;
    },
    changeSize(size) {
      console.log(size);
      if(size=='Bus'){
        this.car_size = 5;
      }
      else if(size=='Car') {
        this.car_size = 2;
      }
      else if(size=='Truck') {
        this.car_size = 7;
      }
      // this.car_size = size;
    },
  },
});
