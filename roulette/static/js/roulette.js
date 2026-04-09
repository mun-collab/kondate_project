document.addEventListener("DOMContentLoaded", () => {
  // ---------------------------------------------------------
  // 1. 変数・要素の準備
  // ---------------------------------------------------------
  const itemCount = document.getElementById("itemCount");
  const genreInput = document.getElementById("genreInput");
  const addGenreBtn = document.getElementById("addGenreBtn");
  const canvas = document.getElementById("wheelCanvas");
  const spinBtn = document.getElementById("spinBtn");
  const resultDisplay = document.getElementById("resultDisplay");
  const itemList = document.getElementById("itemList");
  const startButton = document.getElementById("startButton");
  const backBtn = document.getElementById("backBtn");
  const clearSettings = document.getElementById("clearSettings");

  const ctx = canvas.getContext("2d");
  const radius = canvas.width / 2;

  let genres = [];
  let currentAngle = 0;
  let isSpinning = false;

  const colors = ["#73beff","#ff7474","#5bffd0","#fff04","#a29bfe","#fab1a0","#81ecec","#fd79a8","#e17055","#dfe6e9"];

  // ---------------------------------------------------------
  // 2. リスト操作・描画
  // ---------------------------------------------------------
  function renderList() {
    itemList.innerHTML = "";
    genres.forEach((g, index) => {
      const li = document.createElement("li");
      li.className = "genre-item"
      
      const span = document.createElement("span");
      span.textContent = g;

      const delBtn = document.createElement("button");
      delBtn.type = "button";
      delBtn.textContent = "削除";
      delBtn.className = "delete-btn";
      delBtn.addEventListener("click", () => {
        genres.splice(index, 1);
        renderList();
        drawWheel();
      });

      li.appendChild(span);
      li.appendChild(delBtn);
      itemList.appendChild(li);
    });
  }

  addGenreBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const value = genreInput.value.trim();
    if (!value) return;
    
    // 設定した個数制限のチェック
    const maxCount = Number(itemCount.value);
    if (genres.length >= maxCount) {
      alert(`設定した項目数（${maxCount}個）に達しています`);
      return;
    }
    
    genres.push(value);
    genreInput.value = "";
    renderList();
    drawWheel();
  });

  clearSettings.addEventListener("click", (e) => {
    e.preventDefault();
    if (!confirm("本当に全てのジャンルを削除しますか？")) return;
    genres = [];
    renderList();
    drawWheel();
  });

  // ---------------------------------------------------------
  // 3. ルーレット描画
  // ---------------------------------------------------------
  function drawWheel() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (genres.length === 0) return;
  
    const slice = (Math.PI * 2) / genres.length;
  
    genres.forEach((g, i) => {
      const start = currentAngle + i * slice;
      const end = start + slice;
  
      ctx.beginPath();
      ctx.moveTo(radius, radius);
      ctx.arc(radius, radius, radius, start, end);
      ctx.fillStyle = colors[i % colors.length];
      ctx.fill();
      
  
      ctx.save();
      ctx.translate(radius, radius);
      ctx.rotate(start + slice / 2);
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#333";
      ctx.font = "bold 18px sans-serif";
  
      const characters = g.split("");
      const paddingOuter = 30;
      const charactersSpacing = 20;
  
      characters.forEach((char, index) => {
        const x = radius - paddingOuter - (index * charactersSpacing);
        if (x > 10) { 
          ctx.save();
          ctx.translate(x, 0);
          ctx.rotate(Math.PI / 2);
          ctx.fillText(char, 0, 0);
          ctx.restore();
        }
      });
      ctx.restore();
    });
    
  }

  // 画面切り替えイベント
  startButton.addEventListener("click", () => {
    if (genres.length < 2) {
      alert("2つ以上ジャンルを追加してください");
      return;
    }
    document.getElementById("settings").classList.add("hidden");
    document.getElementById("rouletteArea").classList.remove("hidden");
    drawWheel();
  });

  backBtn.addEventListener("click", () => {
    document.getElementById("rouletteArea").classList.add("hidden");
    document.getElementById("settings").classList.remove("hidden");
  });

  // ---------------------------------------------------------
  // 4. 回転＆結果判定
  // ---------------------------------------------------------
  spinBtn.addEventListener("click", () => {
    if (genres.length < 2 || isSpinning) return;
    isSpinning = true;
    resultDisplay.innerHTML = "抽選中...";
    
    const startRotation = currentAngle;
    const additionalRotation = Math.PI * 8 + Math.random() * Math.PI * 4;
    const duration = 2500;
    const startTime = performance.now();

    function animate(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      currentAngle = startRotation + additionalRotation * easeOut;
      drawWheel();

      if (progress < 1) { 
          requestAnimationFrame(animate); 
      } else { 
          isSpinning = false; 
          determineResult(); 
      }
    }
    requestAnimationFrame(animate);
  });

  function determineResult() {
    const slice = (Math.PI * 2) / genres.length;
    const normalizedAngle = (currentAngle % (Math.PI * 2));
    const needleAngle = (Math.PI * 1.5);
    let index = Math.floor((needleAngle - normalizedAngle) / slice) % genres.length;
    if (index < 0) index += genres.length;
    
    const result = genres[index];
    
    // 1. 結果表示エリアの更新
    resultDisplay.innerHTML = `
      <div style="background: white; padding: 15px; border-radius: 15px; margin-top: 20px; border: 2px solid #4CAF50;">
        <h3 style="margin-bottom: 10px;">🎯 結果：${result}</h3>
        <a href="https://cookpad.com/search/${encodeURIComponent(result)}" 
           target="_blank" style="display: inline-block; background: #FF9800; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: bold;">
           🍳 クックパッドでレシピを探す
        </a>
      </div>
    `;

    // 2. 履歴への自動保存
    saveToHistory(result);

    // 3. HTML側の投稿エリアがある場合に表示する
    const postArea = document.getElementById('post-area');
    const selectedGenreText = document.getElementById('selected-genre');
    if (postArea && selectedGenreText) {
        selectedGenreText.innerText = result;
        postArea.style.display = 'block';
        postArea.scrollIntoView({ behavior: 'smooth' });
    }
  }

  function saveToHistory(genreName) {
      const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
      if (!csrfTokenEl) {
          console.error("CSRFトークンが見つかりません。index.htmlに {% csrf_token %} を記述してください。");
          return;
      }

      fetch("/save_result/", {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfTokenEl.value,
          },
          body: JSON.stringify({
              genre: genreName,
              recipe_url: "",
              memo: ""
          })
      })
      .then(res => res.json())
      .then(data => {
          if (data.status === 'success') {
              console.log("履歴に自動保存されました");
          }
      })
      .catch(err => console.error("履歴保存エラー:", err));
  }

  drawWheel();
});