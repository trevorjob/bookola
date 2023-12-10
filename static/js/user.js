document.addEventListener("DOMContentLoaded", function () {
  // Select elements
  const loaderContainer = document.getElementById("loaderContainer");
  const textContainer = document.getElementById("textContainer");
  const textElement = document.getElementById("text");
  const header = document.querySelector(".title-t");

  header.style.display = "none";
  // Hide loader after 3 seconds
  setTimeout(() => {
    loaderContainer.style.display = "none";
    // Call function to reveal text one letter at a time
    revealText(textElement.textContent);
  }, 3000);
});

function revealText(text) {
  const textElement = document.getElementById("text");
  const header = document.querySelector(".title-t");
  textElement.style.display = "block";
  textElement.textContent = "";
  header.style.display = "block";

  // Split the text into an array of paragraphs
  const paragraphs = text.split("\n");

  // Initialize a counter for the animation
  let paragraphIndex = 0;
  let letterIndex = 0;

  // Function to show letters one after another
  function showLetters() {
    if (paragraphIndex < paragraphs.length) {
      const currentParagraph = paragraphs[paragraphIndex];

      if (letterIndex < currentParagraph.length) {
        const currentLetter = currentParagraph.charAt(letterIndex);
        textElement.innerHTML += currentLetter;
        letterIndex++;
        // Use recursion to continue showing letters
        setTimeout(showLetters, 20);
      } else {
        // Move to the next paragraph
        paragraphIndex++;
        letterIndex = 0;
        // textElement.innerHTML += "<br>"; // Add line break between paragraphs
        // Use recursion to continue showing letters
        setTimeout(showLetters, 20);
      }
    }
  }

  // Start the animation
  showLetters();
}
