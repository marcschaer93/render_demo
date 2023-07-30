

// async function toggleFavoriteStatus(evt) {
//     console.debug("toggleFavoriteStatus");
  
//     const $closestLi = $(evt.target).closest("li");
//     const storyId = $closestLi.attr("id");
//     const story = storyList.stories.find((s) => s.storyId === storyId);
//     const $target = $(evt.target);
  
//     if ($target.hasClass("fa-solid")) {
//       $target.closest("i").toggleClass("fa-solid fa-regular");
//       await currentUser.deleteFavorite(story);
//       putMyFavoritesStoriesOnPage();
//     } else {
//       $target.closest("i").toggleClass("fa-solid fa-regular");
//       await currentUser.addFavorite(story);
//     }
//   }
  
//   $allStoryLists.on("click", ".fa-heart", toggleFavoriteStatus);