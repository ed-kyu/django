<template>
  <div class="container backdrop">
    <Carousel class="mt-4"
    />
    <hr/>
    <recommend class="mt-4">
    </recommend>
    <hr/>
    <recommend2 class="mt-4">
    </recommend2>
    <hr/>
  </div>
</template>

<script>
// @ is an alias to /src
import Carousel from '@/components/Carousel.vue'
import Recommend from '@/components/Recommend.vue'
import Recommend2 from '@/components/Recommend2.vue'
// import Recommend from '@/components/Recommend.vue'

export default {
  name: 'Home',
  components: {
    Carousel,
    Recommend,
    Recommend2,
    // Recommend,
  },
  methods: {
  },
  // created: function () {
  //   this.getMovies()
  // }
}
</script>
<style>
  .backdrop {
    /* background-color: violet; */
    background: 
      linear-gradient(
        to bottom,
        rgba(18, 18, 18, 0) 10%,
        rgba(18, 18, 18, 0.5) 25%,
        rgba(18, 18, 18, 0.7) 40%,
        rgba(18, 18, 18, 1) 50%,
        rgba(18, 18, 18, 1) 75%,
        rgba(18, 18, 18, 1) 100%,
      )
      , url("https://images3.alphacoders.com/948/thumb-1920-948864.jpg");
    background-size: 100%;
    width: 100%;
    min-height: 100%;
    /* background-size: contain; */
  }

</style>