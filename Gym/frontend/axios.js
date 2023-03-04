import Qs from "qs";
import Vue from "vue";
import axios from "axios";
import { NotificationProgrammatic as Notification } from "buefy";

// Заголовок для определения всех запросов к api как ajax
axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

// Использовать свой Serializer
axios.defaults.paramsSerializer = function(params) {
  return Qs.stringify(params, { arrayFormat: "brackets" });
};

// Запись csrf в заголовок для всех запросов
let csrf = document.getElementsByName("csrf-token");
if (csrf.length) {
  axios.defaults.headers.common["X-CSRF-Token"] = csrf[0].getAttribute(
    "content"
  );
}

const flashTypes = {
  info: "is-info",
  error: "is-danger",
  warning: "is-warning",
  success: "is-success"
};

function showFlashes(flashes) {
  Object.entries(flashes).forEach(([variant, messages]) => {
    if (typeof messages == "string") {
      showFlash(variant, messages);
    } else {
      Object.values(messages).forEach(messageString => {
        showFlash(variant, messageString);
      });
    }
  });
}

function showFlash(variant, message) {
  showNotice({
    message: message,
    type: flashTypes[variant],
    duration: 30000
  });
}

function showNotice(config) {
  if (config.title) {
    let message = "<p class='title'>" + config.title + "</p>";
    message += config.message;
    config.message = message;
  }
  config.hasIcon = true;
  config.queue = false;
  Notification.open(config);
}

function handleError(error) {
  let message;
  let type = "is-warning";
  if (error.data instanceof ArrayBuffer) {
    // обработка ошибок при попытке скачать файл
    let enc = new TextDecoder("utf-8");
    let data = JSON.parse(enc.decode(new Uint8Array(error.data)));
    message = data.message;
  } else {
    message = error.data.message;
  }
  if (error.status >= 500) {
    message =
      "<p>Внутренняя ошибка приложения.</p>" +
      "<p>Что-то пошло не так, но мы уже в курсе.</p>";
    type = "is-danger";
  }
  showNotice({
    type: type,
    title: error.status + " " + error.statusText,
    message: message,
    duration: 30000
  });
}

export default function(vueApp) {
  function checkDebugInResponse(response) {
    if (response.headers["x-debug-link"]) {
      vueApp.$store.commit("addResponseDataToDebugStack", {
        status: response.status,
        statusText: response.statusText,
        method: response.config.method,
        url: response.config.url,
        params: response.config.params,
        debugLink: response.headers["x-debug-link"]
      });
    }
  }
  function checkNewVersionInResponse(response) {
    if (response.headers["app-version"]) {
      vueApp.$store.dispatch(
        "checkAppVersion",
        response.headers["app-version"]
      );
    }
  }

  axios.interceptors.response.use(
    response => {
      if (response.data && response.data.flashes) {
        showFlashes(response.data.flashes);
      }
      checkDebugInResponse(response);
      checkNewVersionInResponse(response);
      return response;
    },
    error => {
      if (error.response && error.response.data) {
        handleError(error.response);
      }
      vueApp.$store.commit("fullUnlockContent");
      checkDebugInResponse(error.response);
      return Promise.reject(error.response);
    }
  );
  axios.get("/vue-account/app-version/");
  Vue.prototype.$axios = axios;
}
