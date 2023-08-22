<template>
  <div class="mx-0">
     <h3>
      <!-- TODO : 출력 -->
      <strong>{{ data.sensorA }}</strong> <br />
      <strong>{{ data.sensorB }}</strong> <br />
    </h3>
  </div>
</template>
<script>

import testJSON from "C:/Users/SUN/Desktop/test.json";  // 이 경로만
const data = testJSON; // 

export default {

  mounted(){
  setInterval(()=>{
   //console.log('기본');
  },100); // 주기
  },
  components: {},
  computed: {},
  data() {
    return {
      // data
      data
    };
  }
};
</script>
<style>
</style>