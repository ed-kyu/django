<template>
  <div class="mother-box">
    <div class="d-flex justify-content-center align-items-center">
    <button class="btn btn-sm btn-success mx-2" @click="get_recommend">영화 추천!</button>
    <div class="mx-2">프로필 사진을 등록한 뒤 사용해주세요</div>
    </div>
    <div v-if="recommendCards.length > 0">
      <!-- <h1 class="mt-2">영화 추천</h1> -->
      <h1 class="celebrity mt-3">{{recommendCards[0].celebrity}} {{recommendCards[0].similarity*100}}% 닮으셨네요 </h1>
        <carousel :nav="false" :dots="false" :margin="10" :items="4" class="container top-carousel">
          <div v-for="card in recommendCards" :key="card.id" class="card movieCard mx-1 my-3">
            <!-- <router-link :to="`movie/detail/${card.id}`"> -->
              <img :src="get_path(card)" alt="" class="movieImage">
            <!-- </router-link> -->
          </div>  
        </carousel>
    </div>
    <div v-if="recommendCards.length === 0">
      <h1 class="celebrity mt-3">닮은 영화 배우가 없습니다...</h1>
    </div>
    <!-- <div v-if="notClicked" class="waiting-box">
      <div class="" v-if="Clicked">
      </div>
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
import carousel from 'vue-owl-carousel'
// const SERVER_URL = process.env.VUE_APP_SERVER_URL
// import axios from 'axios'

export default {
  name: "Carousel",
  components: {
    carousel,
  },
  data() {
    return {
      movieCardss : [],
      defaultCards: [],
      notClicked: true,
      // Clicked: false,
    }
  },
  methods: {
    get_path: function(card) {
        return "https://www.themoviedb.org/t/p/w200/" + card.poster_path
    },
    methodThatForcesUpdate() { 
      this.$forceUpdate(); // Notice we have to use a $ here
    },
    get_recommend: function () {
      console.log('추천!', this.$store.state.authUser)
      this.Clicked = true
      this.$store.state.recommendCards = []
        // axios({
        //   method: 'GET',
        //   url: `${SERVER_URL}/accounts/${this.$store.state.authUser.username}/recommendbyprofile/`,
        //   headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        // })
        // .then(res => {
        //   console.log(res.data)
        //   this.movieCardss = res.data
        //   // this.dislikes = res.data.dislikesReceived
        // })
        // .catch(err => {
        //   console.log(err)
        // })
        this.$store.dispatch('LoadRecommendMovies')
        this.notClicked = false
        // this.Clicked = true
      },
  },
  created: function () {
    // this.$store.dispatch('LoadRecommendMovies')
    this.$store.dispatch('LoadGenresNames')
  },
  computed: {
    ...mapState(['recommendCards',]),
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
  /* box-shadow: 0 10px 20px rgba(0,0,0,.12), 0 4px 8px rgba(0,0,0,.06); */
  box-shadow: 0 5px 10px rgba(252, 248, 248, 0.12), 0 4px 8px rgba(0,0,0,.06);

}

.movieCard {
  display: inline-block;
  height: 300px;
  border-style: none;
  background-color: rgb(18, 18, 18);
}

.movieCardSmall {
  display: inline-block;
  height: 200px;
  border-style: none;
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

.celebrity {
  color: white;
}
.mother-box {
  position: relative;
}
.waiting-box {
  position: absolute;
  top: 50px;
  /* left: 100px;
  right: 100px;
  bottom: 200px; */
  z-index: 1;
  color: rgb(38, 230, 140);
  font-size: 40px;
  height: 90%;
  width: 100%;
  background-color: rgb(18, 18, 18);
}
</style>
