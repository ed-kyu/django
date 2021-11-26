<template>
  <div class="" v-if="movieCards.length > 0">
    <h1 class="pt-5 fw-bold">NOW PLAYING</h1> <!--:items="chooseNum"-->
    <div class="demo pt-5" id="demo-4">
      <div class="container coverflow" data-size="180" data-spacing="65" data-shadow="true" data-flat="false" data-bgcolor="#121212">
        <div v-for="card in movieCards" :key="card.id" class="card movieCard"> <!--mx-1 my-3 col-xs-4 col-sm-3 col-md-2-->
          <router-link :to="`movie/detail/${card.id}`">
            <img :src="get_path(card)" class="movieImage">
          </router-link>
        </div>  
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
// import carousel from 'vue-owl-carousel'
import "@/assets/js/coverflow.js"
import "@/assets/style/style.css"

export default {
  name: "Carousel",
  components: {
    // carousel,
  },
  data() {
    return {
      movieCards: null
    }
  },
  methods: {
    get_path: function(card) {
        return "https://www.themoviedb.org/t/p/w200/" + card.poster_path
    },
    methodThatForcesUpdate() { 
      this.$forceUpdate(); // Notice we have to use a $ here
    },
    loadMovieCards() {
      this.movieCards = this.$store.state.movieCards.slice(0, 20)
    },
  },
  created: function () {
    this.$store.dispatch('LoadMovieCards')
    this.$store.dispatch('LoadGenresNames')
    this.loadMovieCards()
  },
  computed: {
    ...mapState(['movieCards',]),
    ...mapState(['genres',]),
  }
}
</script>

<style scoped>
.movieImage {
  transition: all 0.4s;
  border-radius: 5px;
}

.movieImage:hover{
  transform: scale(1.5);
  /* box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06); */
  box-shadow: 0 5px 10px rgba(252, 248, 248, 0.12), 0 4px 8px rgba(0,0,0,.06);
}

.movieCard {
  display: inline-block;
  background-color: rgb(18, 18, 18);
  height: 1000px;
  /* border-radius: 5px; */
  border-style: none;
  /* background-color: gray.100; */
  /* width: 200px; */
}

.owl-carousel .owl-stage {
  display: flex;
}
.owl-carousel .owl-item {
  width: 200px;
}
.owl-carousel .owl-item img {
  width: auto;
  height: 100%;
}

.owl-carousel .nav-btn{
  height: 47px;
  position: absolute;
  width: 26px;
  cursor: pointer;
  top: 100px !important;
}

.owl-carousel .owl-prev.disabled,
.owl-carousel .owl-next.disabled{
pointer-events: none;
opacity: 0.2;
}

.owl-carousel .prev-slide{
  left: -33px;
}
.owl-carousel .next-slide{
  right: -33px;
}
.owl-carousel .prev-slide:hover{
 background-position: 0px -53px;
}
.owl-carousel .next-slide:hover{
background-position: -24px -53px;
}	
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
