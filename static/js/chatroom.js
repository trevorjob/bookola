let socketio = io();
const messages = document.getElementById("messages");
const createMessage = (name, msg, img, time) => {
  const content = `      <div class="s_message">
  <div class="img-div">
    <img
      src="${img}"
      alt=""
    />
  </div>
  <div class="flex_d">
    <div>
      <span class="nm">${name}</span>
      <span class="m_time">${time}</span>
    </div>
    <p class="m_text">
      ${msg}
    </p>
  </div>
</div>
      `;

  messages.innerHTML += content;
};
// const notif = document.querySelector(".notification");

socketio.on("message", (data) => {
  createMessage(data.name, data.message, data.img, data.time);
  //   notif.classList.remove("turn-on");
  //   setTimeout(() => notif.classList.add("turn-on"), 3000);
});
const sendMessage = () => {
  const message = document.getElementById("message");
  if (message.value == "") return;
  //   if (message.value.includes("@")) notif.classList.remove("turn-on");
  socketio.emit("message", { data: message.value });
  message.value = "";
};
