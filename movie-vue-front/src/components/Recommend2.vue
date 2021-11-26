<template>
  <div v-if="movieCards.length > 0">
    <h1 class="mt-2 fw-bold">지금 가장 인기있는 영화</h1> <!--:items="chooseNum"-->
      <carousel :nav="false" :dots="false" :margin="10" :items="4" class="container top-carousel">
        <div v-for="card in movieCards" :key="card.id" class="card movieCard mx-1 my-3"> <!--mx-1 my-3 col-xs-4 col-sm-3 col-md-2-->
          <router-link :to="`movie/detail/${card.id}`">
            <img :src="get_path(card)" alt="" class="movieImage">
          </router-link>
        </div>  
      <!-- <template slot="prev"><span class="prev btn btn-secondary">prev</span></template>
      <template slot="next"><span class="next btn btn-secondary">next</span></template> -->
      <!-- <template slot="{{prev/next}}">ss</template> -->
      </carousel>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import carousel from 'vue-owl-carousel'

export default {
  name: "Carousel",
  components: {
    carousel,
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
      this.movieCards = this.$store.state.movieCards.slice(0, 30)
    },
    popularitySort() {
      this.movieCards.sort(function(a, b){
        return a.popularity - b.popularity
      })
    }
  },
  created: function () {
    this.$store.dispatch('LoadMovieCards')
    this.$store.dispatch('LoadGenresNames')
    this.loadMovieCards()
    this.popularitySort()
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
  transform: scale(1.1);
  /* box-shadow: 0px 1px 2px #c3a0b9, 0 0px 0px #c3a0b9; */
  box-shadow: 0 5px 10px rgba(252, 248, 248, 0.12), 0 4px 8px rgba(0,0,0,.06);
}

.movieCard {
  display: inline-block;
  height: 300px;
  border-style: none;
  background-color: rgb(18, 18, 18);
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
</style>
