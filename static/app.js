/* ---------------- i18n（只翻界面框架，技能内容不翻） ---------------- */
const I18N = {
  zh: {
    "act.pin": "置顶",
    "act.unpin": "取消置顶",
    "ag.sub": "每个 agent 有独立的仓库、全局目录与工作区；切换只影响显示范围，不动任何文件",
    "ag.title": "切换 Agent",
    "agent.settings": "设置",
    "agent.switch": "切换 agent",
    "app.title": "SKILL 本地管理",
    "badge.copies": "共 {n} 份",
    "badge.count": "{n} 个技能",
    "badge.dead": "失效链接",
    "badge.instances": "存在于 {n} 处",
    "badge.linked": "已链接",
    "badge.linkedN": "{n} 个已链接",
    "badge.local": "待纳管",
    "badge.unlinked": "未链接",
    "btn.adopt": "纳入",
    "btn.adoptN": "开始纳管（{n} 个）",
    "btn.cancel": "取消",
    "btn.clone": "复制",
    "btn.close": "关闭",
    "btn.del": "删除",
    "btn.edit": "编辑",
    "btn.hist": "历史",
    "btn.history": "查看全部历史",
    "btn.import": "导入技能",
    "btn.link": "链接",
    "btn.new": "新建",
    "btn.next": "下一步",
    "btn.prev": "上一步",
    "btn.purge": "彻底删除",
    "btn.refresh": "刷新",
    "btn.restore": "恢复",
    "btn.save": "保存",
    "btn.skip": "跳过",
    "btn.start": "开始使用",
    "btn.unlink": "取消链接",
    "card.empty": "（无描述）",
    "card.mtime": "修改于",
    "dlg.delConfirm": "移入回收站",
    "dlg.delNote": "删除时会先移除全部 {n} 处链接，技能移入回收站保留 {d} 天。",
    "dlg.delNoteNone": "技能会移入回收站保留 {d} 天，期间可以恢复。",
    "dlg.delRemove": "仅移除选中链接",
    "dlg.delSub": "这个技能挂在 {n} 个分类下，先确认要移除哪些。",
    "dlg.delSubNone": "这个技能当前没有挂载在任何分类。",
    "dlg.delSubOne": "这个技能挂在「{g}」下。",
    "dlg.delTitle": "删除 {n}",
    "dlg.detachOnly": "只改这一份",
    "dlg.editSave": "保存",
    "dlg.editSaveClose": "保存并关闭",
    "dlg.editTitle": "编辑 {n}",
    "dlg.familyDelete": "同时删除它的分身（共 {n} 份，会合并成回收站里的一条）",
    "dlg.familySync": "这是分身，改动怎么处理？",
    "dlg.familySyncSub": "当前技能还有 {n} 个分身（同源副本）。",
    "dlg.newCreate": "创建",
    "dlg.newDesc": "描述：什么时候用这个技能",
    "dlg.newName": "名称（小写字母、数字、连字符）",
    "dlg.newTitle": "新建技能",
    "dlg.newZh": "中文名（可选）",
    "dlg.syncOnly": "同步到所有分身",
    "empty.hub": "仓库里还没有技能",
    "empty.none": "没有匹配的技能",
    "foot.hub": "已纳入",
    "foot.links": "链接",
    "foot.noLink": "先在左侧选中要链接到的分类",
    "foot.still": "仍在原分组，随时可重新链接",
    "foot.title": "点击打开：",
    "nav.all": "全部",
    "nav.global": "全局SKILL",
    "nav.help": "使用说明",
    "nav.hub": "SKILL仓库（公用）",
    "nav.trash": "回收站",
    "nav.workspaces": "工作区",
    "btn.read": "阅读",
    "btn.copyName": "复制",
    "tt.adoptedN": "{n} 个技能已进仓库，原位置已换成链接",
    "sub.delNote": "里面的 {n} 个技能会回到上级分类，技能本身和挂载都不受影响。",
    "empty.noHist": "这个技能还没有独立记录",
    "trash.deletedAt": "删除于",
    "trash.daysLeft": "剩 {d} 天",
    "trash.linksRemoved": "移除了 {n} 处链接",
    "th.title": "主题",
    "th.sub": "悬停预览 · 点击确认",
    "th.current": "当前",
    "th.black": "曜黑",
    "th.white": "素白",
    "th.amber": "琥珀",
    "th.violet": "紫罗兰",
    "trash.emptyTip": "删除技能后会先移到这里，{d} 天内可以恢复。",
    "trash.noAgent": "未标记来源",
    "trash.restoreMsg": "{n} 已回到仓库（未挂载）{a}；要用的话再挂到目标位置",
    "tab.overview": "概览",
    "tab.links": "链接",
    "tab.history": "历史",
    "tab.gitHistory": "git 历史",
    "sg.newTitle": "新建子分类",
    "sg.renameTitle": "重命名分类",
    "nc.title": "新建空技能",
    "nc.sub": "默认建在 SKILL仓库，SKILL.md 会按标准结构生成（何时使用 / 怎么做 / 示例 / 注意事项），之后拖到分类即可用。",
    "nc.name": "名称（英文，小写）",
    "nc.zh": "中文名",
    "nc.desc": "一句话描述",
    "nc.phZh": "我的技能",
    "nc.phDesc": "什么时候用它",
    "nc.createOnly": "仅创建",
    "nc.createEdit": "创建并编辑",
    "sg.newSub": "会加到「{p}」下面；只是方便分类查看，不影响实际挂载",
    "sg.renameSub": "只改显示名，不影响挂载和归类",
    "sg.create": "创建",
    "sd.title": "删除分类",
    "sd.ok": "删除分类",
    "wp.title": "没找到工作区",
    "wp.skip": "暂时跳过",
    "wp.pick": "选择目录…",
    "ln.current": "当前链接",
    "ln.canLink": "可链接到",
    "ln.notLinked": "尚未链接",
    "wp.note": "你现在的工作区（放项目的那些文件夹）放在哪个目录？",
    "onb.step": "{i} / {n}",
    "pd.adopt": "纳入",
    "rd.copyAll": "复制全文",
    "rd.copyPath": "复制路径",
    "rd.full": "全文",
    "rd.gitNote": "保存后自动提交一条 git 记录",
    "rd.readonly": "只读 · 需要修改点卡片上的「编辑」",
    "rd.saveCommit": "保存并提交",
    "set.add": "添加",
    "set.agents": "Agent 目录",
    "set.cancel": "取消",
    "set.detected": "已检测到",
    "set.fmt": "格式",
    "set.global": "全局目录",
    "set.hub": "仓库",
    "set.hubShared": "共用 data/hub（所有 agent 一份）",
    "set.name": "显示名称",
    "set.parent": "父目录",
    "set.parentPh": "你的工作区父目录",
    "set.rescan": "保存并重扫",
    "set.rules": "rules 格式",
    "set.saveBtn": "保存",
    "set.skillsN": "{n} 个技能",
    "set.sub": "勾选要管理的 agent，确认它们的技能目录。识别不到时可以手动填路径；每个 agent 有独立仓库。",
    "set.sub2": "勾选要管理的 agent，确认它们的技能目录。识别不到时可以手动填路径。",
    "set.title": "Agent 设置",
    "set.undetected": "未检测到",
    "set.wsAddPh": "手动添加一个工作区路径（含 .dsh/skills）",
    "set.wsEmpty": "没有发现工作区。把父目录改成你放项目的目录，或在下面手动添加。",
    "set.wsSection": "工作区检测",
    "sort.name": "按名称",
    "sort.size": "按大小",
    "sort.time": "按修改时间",
    "toast.clone": "已复制",
    "toast.cloneMsg": "{a} → {b}（内容相同，可挂到别的 agent）",
    "toast.cloned": "已复制",
    "toast.copied": "已复制",
    "toast.delMsg": "{n} 已移入回收站 · {d} 天后彻底删除",
    "toast.deleted": "已移入回收站",
    "toast.failed": "失败",
    "toast.family": "（含分身，已合并为一条）",
    "toast.linkMsg": "{n} → {g}",
    "toast.linked": "已链接",
    "toast.restoreMsg": "{n} 已回到仓库（未挂载）",
    "toast.restored": "已恢复",
    "toast.saved": "已保存",
    "toast.unlinkMsg": "{n} 取消了 {g} 的挂载",
    "toast.unlinked": "已取消链接",
    "trash.empty": "回收站是空的",
    "trash.emptySub": "空的 · 删除的技能会在这里保留 {d} 天",
    "trash.sub": "{n} 个已删除 · 保留 {d} 天，到期自动彻底删除",
    "tt.0": "保存失败",
    "tt.1": "打开失败",
    "tt.10": "恢复失败",
    "tt.11": "纳管部分完成",
    "tt.12": "纳管失败",
    "tt.13": "纳管完成",
    "tt.14": "切换失败",
    "tt.15": "请选目标",
    "tt.16": "删除失败",
    "tt.17": "设置失败",
    "tt.18": "失败",
    "tt.19": "刷新失败",
    "tt.2": "导入不可用",
    "tt.20": "添加失败",
    "tt.21": "未选择",
    "tt.22": "无法打开选择框",
    "tt.23": "移动失败",
    "tt.24": "已保存",
    "tt.25": "已彻底删除",
    "tt.26": "已创建",
    "tt.27": "已创建分类",
    "tt.28": "已存在",
    "tt.29": "已打开",
    "tt.3": "导入失败",
    "tt.30": "已导入",
    "tt.31": "已调整顺序",
    "tt.32": "已断开原分组",
    "tt.33": "已复制",
    "tt.34": "已更新工作区父目录",
    "tt.35": "已归类",
    "tt.36": "已恢复到 SKILL仓库",
    "tt.37": "已链接",
    "tt.38": "已切换",
    "tt.39": "已取消链接",
    "tt.4": "调整失败",
    "tt.40": "已删除分类",
    "tt.41": "已设置",
    "tt.42": "已收回",
    "tt.43": "已刷新",
    "tt.44": "已添加工作区",
    "tt.45": "已移除链接",
    "tt.46": "已移入回收站",
    "tt.47": "已重命名",
    "tt.48": "主题已切换",
    "tt.5": "读取失败",
    "tt.6": "发现新技能",
    "tt.7": "复制失败",
    "tt.8": "更新失败",
    "tt.9": "归类失败"
  },
  en: {
    "act.pin": "Pin",
    "act.unpin": "Unpin",
    "ag.sub": "Each agent has its own global dir and workspace mounts. Switching only changes what you see — no files are touched.",
    "ag.title": "Switch agent",
    "agent.settings": "Settings",
    "agent.switch": "Switch agent",
    "app.title": "SKILL Manager",
    "badge.copies": "{n} copies",
    "badge.count": "{n} skills",
    "badge.dead": "Broken link",
    "badge.instances": "in {n} places",
    "badge.linked": "Linked",
    "badge.linkedN": "{n} linked",
    "badge.local": "Pending",
    "badge.unlinked": "In hub",
    "btn.adopt": "Adopt",
    "btn.adoptN": "Adopt {n} skills",
    "btn.cancel": "Cancel",
    "btn.clone": "Copy",
    "btn.close": "Close",
    "btn.del": "Delete",
    "btn.edit": "Edit",
    "btn.hist": "History",
    "btn.history": "History",
    "btn.import": "Import",
    "btn.link": "Link",
    "btn.new": "New",
    "btn.next": "Next",
    "btn.prev": "Back",
    "btn.purge": "Delete forever",
    "btn.refresh": "Refresh",
    "btn.restore": "Restore",
    "btn.save": "Save",
    "btn.skip": "Skip",
    "btn.start": "Start",
    "btn.unlink": "Unlink",
    "card.empty": "(no description)",
    "card.mtime": "modified",
    "dlg.delConfirm": "Move to trash",
    "dlg.delNote": "All {n} links are removed first, then the skill goes to trash for {d} days.",
    "dlg.delNoteNone": "The skill goes to trash and stays recoverable for {d} days.",
    "dlg.delRemove": "Remove selected links",
    "dlg.delSub": "Linked in {n} places — confirm which to remove.",
    "dlg.delSubNone": "这个技能当前没有挂载在任何分类。",
    "dlg.delSubOne": "Linked under \\\",\n    ",
    "dlg.delTitle": "Delete {n}",
    "dlg.detachOnly": "Only this one",
    "dlg.editSave": "Save",
    "dlg.editSaveClose": "Save & close",
    "dlg.editTitle": "Edit {n}",
    "dlg.familyDelete": "Also delete its copies ({n} total, merged into one trash entry)",
    "dlg.familySync": "This skill has copies — what to do?",
    "dlg.familySyncSub": "{n} copies share this content.",
    "dlg.newCreate": "Create",
    "dlg.newDesc": "Description: when to use it",
    "dlg.newName": "Name (lowercase, digits, hyphen)",
    "dlg.newTitle": "New skill",
    "dlg.newZh": "Chinese name (optional)",
    "dlg.syncOnly": "Sync to all copies",
    "empty.hub": "Hub is empty",
    "empty.none": "No matching skills",
    "foot.hub": "in hub",
    "foot.links": "links",
    "foot.noLink": "Pick a category on the left to link into",
    "foot.still": "Still in its group, can be relinked anytime",
    "foot.title": "Open: ",
    "nav.all": "All",
    "nav.global": "Global",
    "nav.help": "Guide",
    "nav.hub": "SKILL Hub (shared)",
    "nav.trash": "Trash",
    "nav.workspaces": "Workspaces",
    "btn.read": "Read",
    "btn.copyName": "Copy",
    "tt.adoptedN": "{n} skills moved into the hub; links created in place",
    "sub.delNote": "{n} skills inside will move back to the parent; files and links are unaffected.",
    "empty.noHist": "No history for this skill yet",
    "trash.deletedAt": "deleted",
    "trash.daysLeft": "{d} days left",
    "trash.linksRemoved": "{n} links removed",
    "th.title": "Theme",
    "th.sub": "Hover to preview · click to apply",
    "th.current": "current",
    "th.black": "Black",
    "th.white": "White",
    "th.amber": "Amber",
    "th.violet": "Violet",
    "trash.emptyTip": "Deleted skills land here and stay recoverable for {d} days.",
    "trash.noAgent": "source unknown",
    "trash.restoreMsg": "{n} is back in the hub (not linked){a}. Link it again where you need it.",
    "tab.overview": "Overview",
    "tab.links": "Links",
    "tab.history": "History",
    "tab.gitHistory": "git history",
    "sg.newTitle": "New group",
    "sg.renameTitle": "Rename group",
    "nc.title": "New empty skill",
    "nc.sub": "Created in the SKILL Hub with the standard SKILL.md skeleton (when to use / how / examples / notes). Drag it to a section to activate.",
    "nc.name": "Name (lowercase english)",
    "nc.zh": "Chinese name",
    "nc.desc": "One-line description",
    "nc.phZh": "my skill",
    "nc.phDesc": "when to use it",
    "nc.createOnly": "Create",
    "nc.createEdit": "Create & edit",
    "sg.newSub": "Added under {p}. It is only a view grouping — links are unaffected.",
    "sg.renameSub": "Only the display name changes; links and grouping stay the same.",
    "sg.create": "Create",
    "sd.title": "Delete group",
    "sd.ok": "Delete group",
    "wp.title": "No workspace found",
    "wp.skip": "Skip for now",
    "wp.pick": "Choose folder…",
    "ln.current": "Currently linked",
    "ln.canLink": "Can link to",
    "ln.notLinked": "not linked",
    "wp.note": "Where do you keep your workspaces (the folders holding your projects)?",
    "onb.step": "{i} / {n}",
    "pd.adopt": "Adopt",
    "rd.copyAll": "Copy all",
    "rd.copyPath": "Copy path",
    "rd.full": "Full text",
    "rd.gitNote": "Saving creates one git commit",
    "rd.readonly": "Read-only · use Edit on the card to change",
    "rd.saveCommit": "Save & commit",
    "set.add": "Add",
    "set.agents": "Agent directories",
    "set.cancel": "Cancel",
    "set.detected": "detected",
    "set.fmt": "Format",
    "set.global": "Global dir",
    "set.hub": "Store",
    "set.hubShared": "shared data/hub (one for all agents)",
    "set.name": "Display name",
    "set.parent": "Parent dir",
    "set.parentPh": "Your workspace parent dir",
    "set.rescan": "Save & rescan",
    "set.rules": "rules format",
    "set.saveBtn": "Save",
    "set.skillsN": "{n} skills",
    "set.sub": "Pick the agents to manage and confirm their skill dirs. Unknown paths can be filled in manually; each agent has its own hub.",
    "set.sub2": "Pick the agents to manage and confirm their skill dirs. Unknown paths can be filled in manually.",
    "set.title": "Agent Settings",
    "set.undetected": "not found",
    "set.wsAddPh": "Add a workspace path (must contain .dsh/skills)",
    "set.wsEmpty": "No workspace found. Point the parent dir at where your projects live, or add one below.",
    "set.wsSection": "Workspace detection",
    "sort.name": "Name",
    "sort.size": "Size",
    "sort.time": "Modified",
    "toast.clone": "Copied",
    "toast.cloneMsg": "{a} → {b} (same content, can target another agent)",
    "toast.cloned": "Copied",
    "toast.copied": "Copied",
    "toast.delMsg": "{n} moved to trash · auto-deleted in {d} days",
    "toast.deleted": "Moved to trash",
    "toast.failed": "Failed",
    "toast.family": " (with copies, merged into one entry)",
    "toast.linkMsg": "{n} → {g}",
    "toast.linked": "Linked",
    "toast.restoreMsg": "{n} is back in the hub (not linked)",
    "toast.restored": "Restored",
    "toast.saved": "Saved",
    "toast.unlinkMsg": "{n} unlinked from {g}",
    "toast.unlinked": "Unlinked",
    "trash.empty": "Trash is empty",
    "trash.emptySub": "Empty · deleted skills stay here for {d} days",
    "trash.sub": "{n} deleted · kept {d} days",
    "tt.0": "Save failed",
    "tt.1": "Open failed",
    "tt.10": "Restore failed",
    "tt.11": "Partly adopted",
    "tt.12": "Adopt failed",
    "tt.13": "Adopted",
    "tt.14": "Switch failed",
    "tt.15": "Pick a target",
    "tt.16": "Delete failed",
    "tt.17": "Setup failed",
    "tt.18": "Failed",
    "tt.19": "Refresh failed",
    "tt.2": "Import unavailable",
    "tt.20": "Add failed",
    "tt.21": "Nothing selected",
    "tt.22": "Cannot open picker",
    "tt.23": "Move failed",
    "tt.24": "Saved",
    "tt.25": "Permanently deleted",
    "tt.26": "Created",
    "tt.27": "Group created",
    "tt.28": "Already exists",
    "tt.29": "Opened",
    "tt.3": "Import failed",
    "tt.30": "Imported",
    "tt.31": "Reordered",
    "tt.32": "Ungrouped",
    "tt.33": "Copied",
    "tt.34": "Workspace parent updated",
    "tt.35": "Grouped",
    "tt.36": "Restored to hub",
    "tt.37": "Linked",
    "tt.38": "Switched",
    "tt.39": "Unlinked",
    "tt.4": "Reorder failed",
    "tt.40": "Group deleted",
    "tt.41": "Done",
    "tt.42": "Recalled",
    "tt.43": "Refreshed",
    "tt.44": "Workspace added",
    "tt.45": "Links removed",
    "tt.46": "Moved to trash",
    "tt.47": "Renamed",
    "tt.48": "Theme changed",
    "tt.5": "Read failed",
    "tt.6": "New skills found",
    "tt.7": "Copy failed",
    "tt.8": "Update failed",
    "tt.9": "Group failed"
  },
};

let LANG = localStorage.getItem("lang") || "zh";
document.documentElement.lang = LANG === "en" ? "en" : "zh-CN";

function t(key, vars) {
  const dict = I18N[LANG] || I18N.zh;
  let v = dict[key] ?? I18N.zh[key] ?? key;
  if (vars) {
    for (const k of Object.keys(vars)) v = v.replaceAll("{" + k + "}", vars[k]);
  }
  return v;
}

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    el.placeholder = t(el.dataset.i18nPh);
  });
  const ph = document.getElementById("q");
  if (ph && LANG === "en") ph.placeholder = "Search skills…";
  if (ph && LANG === "zh") ph.placeholder = "搜索技能…";
}

function setLang(lang) {
  LANG = lang === "en" ? "en" : "zh";
  localStorage.setItem("lang", LANG);
  document.documentElement.lang = LANG === "en" ? "en" : "zh-CN";
  const b = document.getElementById("btnLang");
  if (b) b.textContent = LANG === "en" ? "EN" : "中";
  applyI18n();
  if (typeof renderNav === "function") renderNav();
  if (typeof render === "function") render();
  if (typeof renderPending === "function") renderPending();
  if (typeof syncStats === "function") syncStats();
  if (typeof current !== "undefined" && current === "trash" && typeof renderTrash === "function") renderTrash();
}

/* SKILL本地管理 · 前端逻辑 */
const THEMES = ["black", "white", "amber", "violet"];
const THEME_LABELS = { black: "纯黑", white: "纯白", amber: "琥珀橙", violet: "紫罗兰" };

let STATE = { roots: [], skills: [], history: [], config: {} };
let curTheme = "black";
let current = "all";
let query = "";
let pendingExpanded = false;
let dragSkill = null;
let pendingMove = null;
let currentSkill = null;

/* ---------------- 主题 ---------------- */
function applyThemeIcon(t) {
  const img = document.querySelector(".tb-logo");
  if (img) img.src = "/static/icon-" + t + "-128.png?v=2";
  const fav = document.querySelector('link[rel="icon"]');
  if (fav) fav.href = "/static/icon-" + t + "-128.png?v=2";
}
function setTheme(t) {
  curTheme = t;
  document.documentElement.setAttribute("data-theme", t);
  applyThemeIcon(t);
  fetch("/api/theme", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ theme: t }),
  }).catch(() => {});
}

/* 主题选择器：悬停即时预览，点击确认，取消还原 */
let themeBackup = "black";

function openThemePicker() {
  if (document.getElementById("themePicker")) return;
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");  // 别让上一条提示挡住弹窗
  themeBackup = curTheme;
  const box = document.createElement("div");
  box.id = "themePicker";
  box.innerHTML = `
    <div class="th-overlay"></div>
    <div class="th-modal">
      <div class="th-head">
        <span class="th-title">${t("th.title")}</span>
        <span class="th-sub">${t("th.sub")}</span>
        <span class="th-close" id="thClose">✕</span>
      </div>
      <div class="th-grid">
        ${THEMES.map((th) => `
          <div class="th-item${th === curTheme ? " on" : ""}" data-t="${th}">
            <div class="th-swatch sw-${th}"><i></i><i></i><i></i></div>
            <div class="th-name">${t("th." + th)}${th === curTheme ? ` <em>${t("th.current")}</em>` : ""}</div>
          </div>`).join("")}
      </div>
    </div>`;
  document.body.appendChild(box);

  function onKey(e) {
    if (e.key === "Escape") closePicker(null);
  }
  function closePicker(pick) {
    box.remove();
    document.removeEventListener("keydown", onKey);
    if (pick) {
      setTheme(pick);
      showToast(t("tt.48"), t("th." + pick));
    } else {
      document.documentElement.setAttribute("data-theme", themeBackup);
    }
  }

  box.querySelectorAll(".th-item").forEach((el) => {
    el.onmouseenter = () => document.documentElement.setAttribute("data-theme", el.dataset.t);
    el.onclick = () => closePicker(el.dataset.t);
  });
  box.querySelector(".th-overlay").onclick = () => closePicker(null);
  box.querySelector("#thClose").onclick = () => closePicker(null);
  document.addEventListener("keydown", onKey);
}

let sortBy = "name";
let pendingDismissed = false;
try {
  sortBy = localStorage.getItem("skillmgr.sort") || "name";
  pendingDismissed = localStorage.getItem("skillmgr.pendingHidden") === "1";
} catch (_) {}

function fmtTime(ts) {
  if (!ts) return "";
  const d = new Date(ts * 1000);
  const p = (n) => String(n).padStart(2, "0");
  return `${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function showDragTip(main, sub, warn) {
  const el = document.getElementById("dragTip");
  if (!el) return;
  document.getElementById("dtMain").textContent = main;
  document.getElementById("dtSub").textContent = sub || "";
  el.classList.toggle("warn", !!warn);
  el.classList.add("on");
}

function hideDragTip() {
  const el = document.getElementById("dragTip");
  if (el) el.classList.remove("on");
}

/* 插入 HTML 前统一转义，避免名字里的 < " 破版 */
function esc(v) {
  return String(v == null ? "" : v).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

/* ---------------- 回收站 ---------------- */
function agentNameOf(id) {
  if (!id) return "";
  const a = (Array.isArray(STATE.agents) ? STATE.agents : []).find((x) => x.id === id);
  return a ? a.label : id;
}

function renderTrash() {
  const rawItems = STATE.trash || [];
  // 同 familyId 合并成一条（连带删除分身时产生）
  const grouped = [];
  const seenFam = new Map();
  rawItems.forEach((it) => {
    if (it.familyId) {
      if (seenFam.has(it.familyId)) {
        const g = seenFam.get(it.familyId);
        g.ids.push(it.id);
        g.names.push(it.name);
        g.sizeKb += it.sizeKb || 0;
        return;
      }
      const merged = { ...it, name: (it.familyNames && it.familyNames[0]) || it.name,
                       ids: [it.id], names: it.familyNames && it.familyNames.length ? [...it.familyNames] : [it.name] };
      seenFam.set(it.familyId, merged);
      grouped.push(merged);
      return;
    }
    grouped.push({ ...it, ids: [it.id], names: [it.name] });
  });
  const items = grouped;
  const days = STATE.trashDays || 10;
  document.getElementById("viewTitle").textContent = t("nav.trash");
  document.getElementById("viewSub").textContent = items.length
    ? t("trash.sub", { n: items.length, d: days })
    : t("trash.emptySub", { d: days });
  const grid = document.getElementById("grid");
  if (!items.length) {
    grid.innerHTML = `<div class="empty"><h3>${t("trash.empty")}</h3><p>${t("trash.emptyTip", { d: days })}</p></div>`;
    return;
  }
  grid.innerHTML = items
    .map(
      (it) => `<div class="card glass trash-card" data-tid="${esc(it.ids[0])}">
        <div class="card-head">
          <div style="display:flex;gap:12px;align-items:flex-start">
            <div class="ico g-trash">${esc((it.name || "?").slice(0, 1).toUpperCase())}</div>
            <h3>${esc(it.name)}${it.nameZh ? `<span class="cn">${esc(it.nameZh)}</span>` : ""}</h3>
          </div>
        </div>
        <div class="desc">${esc(it.desc) || t("card.empty")}</div>
        <div class="badges">
          ${it.agent ? `<span class="badge b-count">${esc(agentNameOf(it.agent))}</span>` : `<span class="badge b-off">${t("trash.noAgent")}</span>`}
          <span class="badge b-off">${t("trash.deletedAt")} ${fmtTime(it.deletedAt)}</span>
          <span class="badge b-count">${t("trash.daysLeft", { d: it.daysLeft })}</span>
          ${it.links?.length ? `<span class="badge b-off">${t("trash.linksRemoved", { n: it.links.length })}</span>` : ""}
          <span class="badge b-off">${it.sizeKb || 0} KB</span>
        </div>
        <div class="card-foot">
          <span class="mini link" data-restore="${esc(it.ids[0])}">${t("btn.restore")}</span>
          <span class="mini danger" data-purge="${esc(it.ids[0])}">${t("btn.purge")}</span>
          <span class="mtime">${fmtTime(it.deletedAt)}</span>
        </div>
      </div>`
    )
    .join("");
  grid.querySelectorAll("[data-restore]").forEach((b) => {
    b.onclick = async () => {
      try {
        const d = await api("/api/trash/restore", { method: "POST", body: JSON.stringify({ id: b.dataset.restore }) });
        await refresh(d.state);
        const label = d.agentLabel || agentNameOf(d.agent) || d.agent || "";
        showToast(t("tt.36"), t("trash.restoreMsg", { n: d.name, a: label ? " (" + label + ")" : "" }));
      } catch (e) {
        showToast(t("tt.10"), e.message);
      }
    };
  });
  grid.querySelectorAll("[data-purge]").forEach((b) => {
    b.onclick = async () => {
      const t = (STATE.trash || []).find((x) => x.id === b.dataset.purge);
      if (!confirm(`彻底删除「${t?.name || "这一项"}」？这一步不能恢复。`)) return;
      try {
        const d = await api("/api/trash/purge", { method: "POST", body: JSON.stringify({ id: b.dataset.purge }) });
        await refresh(d.state);
        showToast(t("tt.25"), t?.name || "");
      } catch (e) {
        showToast(t("tt.16"), e.message);
      }
    };
  });
}

/* ---------------- Agent 切换 ---------------- */
function openAgentPicker() {
  if (document.getElementById("agentPicker")) return;
  const raw = STATE.agents;
  const list = Array.isArray(raw) ? raw : [];
  const active = STATE.activeAgent;
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const box = document.createElement("div");
  box.id = "agentPicker";
  box.innerHTML = `
    <div class="overlay on" id="apOverlay"></div>
    <div class="lp on" id="apBox">
      <div class="lp-head">
        <div class="lp-badge">⇄</div>
        <div>
          <div class="lp-title">${t("ag.title")}</div>
          <div class="lp-sub">${t("ag.sub")}</div>
        </div>
      </div>
      <div class="lp-body">
        <div class="ap-list">
          ${list
            .map(
              (a) => `<div class="ap-item${a.id === active ? " on" : ""}" data-id="${esc(a.id)}">
                <span class="ap-name">${esc(a.label)}</span>
                <span class="ap-id">${esc(a.id)}</span>
              </div>`
            )
            .join("")}
        </div>
      </div>
      <div class="lp-acts">
        <div class="btn ghost" id="apCancel">${t("btn.close")}</div>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#apOverlay").onclick = close;
  box.querySelector("#apCancel").onclick = close;
  box.querySelectorAll(".ap-item").forEach((el) => {
    el.onclick = async () => {
      const id = el.dataset.id;
      if (id === active) {
        close();
        return;
      }
      try {
        const d = await api("/api/agent", { method: "POST", body: JSON.stringify({ id }) });
        close();
        STATE = d.state;
        current = "all";
        collapsedKeys.clear();
        saveCollapsed();
        renderNav();
        render();
        renderPending();
        syncStats();
        showToast(t("tt.38"), `当前 agent：${agentLabel()}`);
      } catch (e) {
        showToast(t("tt.14"), e.message);
      }
    };
  });
}

/* ---------------- Agent 设置 ---------------- */
async function openAgentSettings() {
  if (document.getElementById("asBox")) return;
  let data;
  let ws;
  try {
    data = await fetch("/api/agents/candidates").then((r) => r.json());
    ws = await fetch("/api/workspaces").then((r) => r.json());
  } catch (e) {
    showToast(t("tt.5"), e.message);
    return;
  }
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const box = document.createElement("div");
  box.id = "asWrap";
  box.innerHTML = `
    <div class="overlay on" id="asOverlay"></div>
    <div class="lp on" id="asBox">
      <div class="lp-head">
        <div class="lp-badge">⚙</div>
        <div>
          <div class="lp-title">${t("set.title")}</div>
          <div class="lp-sub">${t("set.sub2")}</div>
        </div>
      </div>
      <div class="lp-body">
        <div class="as-section">${t("set.wsSection")}</div>
        <div class="as-wsparent">
          <span class="as-k">${t("set.parent")}</span>
          <input class="as-wsinput" id="asWsParent" value="${esc(ws.parent)}" placeholder="${t("set.parentPh")}">
          <button class="btn ghost" id="asWsSave" style="padding:6px 12px;font-size:12.5px">${t("set.rescan")}</button>
        </div>
        <div class="as-wslist">
          ${(ws.items || []).length
            ? ws.items.map((w) => `<div class="as-wsrow"><span class="nm">${esc(w.name)}</span><span class="pt">${esc(w.path)}</span><span class="ct">${t("set.skillsN", { n: w.skills })}</span></div>`).join("")
            : `<div class="as-wsempty">${t("set.wsEmpty")}</div>`}
        </div>
        <div class="as-wsrow" style="margin-top:8px">
          <input class="as-wsinput" id="asWsAdd" placeholder="${t("set.wsAddPh")}">
          <button class="btn ghost" id="asWsAddBtn" style="padding:6px 12px;font-size:12.5px">${t("set.add")}</button>
        </div>
        <div class="as-section" style="margin-top:16px">${t("set.agents")}</div>
        <div class="as-list">
          ${(data.items || [])
            .map(
              (it) => `<div class="as-item" data-id="${esc(it.id)}">
              <label class="as-check"><input type="checkbox" ${it.enabled ? "checked" : ""}></label>
              <div class="as-main">
                <div class="as-row1">
                  <input class="as-label" value="${esc(it.label)}" placeholder="${t("set.name")}">
                  <span class="as-tag${it.detected ? " on" : ""}">${it.detected ? t("set.detected") : t("set.undetected")}</span>
                  ${it.format === "rules" ? `<span class="as-tag warn">${t("set.rules")}</span>` : ""}
                </div>
                <div class="as-row2"><span class="as-k">${t("set.global")}</span>
                  <input class="as-g" value="${esc(it.globalSkillsDir)}" placeholder="~/.xxx/skills"></div>
                <div class="as-row2"><span class="as-k">${t("set.hub")}</span>
                  <span class="as-fixed">${t("set.hubShared")}</span></div>
              </div>
            </div>`
            )
            .join("")}
        </div>
      </div>
      <div class="lp-acts">
        <div class="btn ghost" id="asCancel">${t("set.cancel")}</div>
        <div class="btn primary" id="asSave">${t("dlg.editSave")}</div>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#asOverlay").onclick = close;
  box.querySelector("#asCancel").onclick = close;
  const wsSave = box.querySelector("#asWsSave");
  if (wsSave) wsSave.onclick = async () => {
    const p = box.querySelector("#asWsParent").value.trim();
    try {
      const d = await api("/api/workspace-parent", { method: "POST", body: JSON.stringify({ path: p }) });
      STATE = d.state;
      current = "all";
      renderNav();
      render();
      syncStats();
      close();
      showToast(t("tt.34"), p);
    } catch (e) {
      showToast(t("tt.8"), e.message);
    }
  };
  const wsAdd = box.querySelector("#asWsAddBtn");
  if (wsAdd) wsAdd.onclick = async () => {
    const p = box.querySelector("#asWsAdd").value.trim();
    if (!p) return;
    try {
      const cur = await fetch("/api/workspaces").then((r) => r.json());
      const list = (cur.items || []).map((x) => x.path);
      if (!list.includes(p)) list.push(p);
      const d = await api("/api/workspaces", { method: "POST", body: JSON.stringify({ workspaces: list }) });
      STATE = d.state;
      current = "all";
      renderNav();
      render();
      syncStats();
      close();
      showToast(t("tt.44"), p);
    } catch (e) {
      showToast(t("tt.20"), e.message);
    }
  };
  box.querySelector("#asSave").onclick = async () => {
    const items = [...box.querySelectorAll(".as-item")].map((el) => ({
      id: el.dataset.id,
      enabled: el.querySelector("input[type=checkbox]").checked,
      label: el.querySelector(".as-label").value,
      globalSkillsDir: el.querySelector(".as-g").value,

    }));
    try {
      const d = await api("/api/agents/save", { method: "POST", body: JSON.stringify({ items }) });
      close();
      if (d.state) {
        STATE = d.state;
        current = "all";
        collapsedKeys.clear();
        saveCollapsed();
        renderNav();
        render();
        renderPending();
        syncStats();
      }
      showToast(t("tt.24"), `当前 agent：${agentLabel()}`);
    } catch (e) {
      showToast(t("tt.0"), e.message);
    }
  };
}

/* ---------------- 分组 ---------------- */
function groupLabel(key) {
  if (key === "all") return "全部";
  if (key === "hub") return "SKILL仓库（公用）";
  if (key === "global") return "全局SKILL";
  if (key.startsWith("sg:")) {
    const g = (STATE.config?.subGroups || []).find((x) => "sg:" + x.id === key);
    return g ? g.name : "分类";
  }
  const r = STATE.roots.find((x) => x.key === key);
  return r ? r.label : key;
}
function groupOf(s) {
  if (s.group === "hub") return "hub";
  if (s.group === "global") return "global";
  return s.group;
}

/* ---------------- 渲染 ---------------- */
function zhOf(s) {
  if (s.nameZh && s.nameZh !== s.name) return s.nameZh;
  if (/[\u4e00-\u9fa5]/.test(s.name || "")) return "";
  const d = s.desc || "";
  return /[\u4e00-\u9fa5]/.test(d) ? d.slice(0, 12) : "";
}

function statusBadge(s) {
  if (s.status === "linked") return `<span class="badge b-ok">${t("badge.linked")}</span>`;
  if (s.status === "unlinked") return `<span class="badge b-off">${t("badge.unlinked")}</span>`;
  if (s.status === "dead") return `<span class="badge b-warn">${t("badge.dead")}</span>`;
  return `<span class="badge b-warn">${t("badge.local")}</span>`;
}

function navItems() {
  const items = [
    { key: "all", label: t("nav.all") },
    { key: "hub", label: t("nav.hub") },
    { key: "global", label: t("nav.global") },
  ];
  (STATE.config?.subGroups || []).forEach((g) =>
    items.push({ key: "sg:" + g.id, label: g.name, sub: true, parent: g.parent || "global" })
  );
  STATE.roots
    .filter((r) => r.kind === "workspace")
    .forEach((r) => items.push({ key: r.key, label: r.label }));
  return items;
}

function belongsTo(s, key) {
  if (key === "all") return true;
  if (key === "hub") return groupOf(s) === "hub";
  if (key.startsWith("sg:")) {
    return ((STATE.config?.skillGroups || {})[s.name] || "") === key.slice(3);
  }
  if ((s.links || []).some((l) => l.root === key)) return true;
  return groupOf(s) === key;
}

function countOf(key) {
  return STATE.skills.filter((s) => belongsTo(s, key)).length;
}

function agentLabel() {
  const list = STATE.agents || [];
  if (!Array.isArray(list)) return "DSH";
  const a = list.find((x) => x.id === STATE.activeAgent);
  return a ? a.label : "DSH";
}

function navItemHtml(it, extra) {
  const active = it.key === current ? " active" : "";
  const folded = collapsedKeys.has(it.key);
  const foldable = it.key !== "all";
  const fold = foldable
    ? `<button class="nav-fold${folded ? " collapsed" : ""}" data-fold="${it.key}" title="展开/收起">▸</button>`
    : "";
  const add =
    it.key === "global" || it.key === "hub"
      ? `<button class="nav-add" data-add="${it.key}" title="新建子分类">＋</button>`
      : "";
  const agentBtn = "";
  return `<div class="nav-item${active}${extra || ""}" data-g="${esc(it.key)}" title="${esc(it.label)}">
        <span class="lbl">${fold}<span class="lbl-t">${esc(it.label)}</span><span class="cnt">${countOf(it.key)}</span></span>
        <span class="nav-right">${agentBtn}${add}</span>
      </div>`;
}

function bindNavItems(el) {
  el.querySelectorAll(".nav-item").forEach((item) => {
    const g = item.dataset.g;
    item.onclick = (e) => {
      if (e.target.closest(".nav-fold,.nav-add,.nav-del,[data-fold],[data-sg]")) return;
      current = g;
      if (g !== "all" && g !== "trash") {
        if (collapsedKeys.has(g)) collapsedKeys.delete(g);
        else collapsedKeys.add(g);
        saveCollapsed();
      }
      renderNav();
      render();
    };
    if (g === "all" || g === "trash" || g === "help") return;
    item.ondragover = (e) => {
      e.preventDefault();
      item.classList.add("drop-hover");
      if (subDrag) {
        const dstParent = g === "hub" ? "SKILL仓库" : "全局SKILL";
        showDragTip(`移动分类到「${dstParent}」`, "只改分类归属，不影响挂载", false);
      } else if (g === "hub") {
        showDragTip("放回 SKILL仓库", "会断开该技能的所有挂载", true);
      } else if (g.startsWith("sg:")) {
        showDragTip(`归类到「${groupLabel(g)}」`, "只是查看分类，不影响挂载", false);
      } else {
        showDragTip(`移动到「${groupLabel(g)}」`, "会改变挂载位置，新对话生效", true);
      }
    };
    item.ondragleave = () => {
      item.classList.remove("drop-hover");
    };
    item.ondrop = (e) => {
      e.preventDefault();
      item.classList.remove("drop-hover");
      hideDragTip();
      if (subDrag) {
        const dstParent = g === "hub" ? "hub" : g === "global" ? "global" : "";
        if (dstParent) {
          const moved = subDrag;
          subDrag = null;
          moveSub(moved.id, dstParent, null);
        }
        return;
      }
      onDrop(g, e);
    };
  });
  el.querySelectorAll("[data-fold]").forEach((b) => {
    b.onclick = (e) => {
      e.stopPropagation();
      const k = b.dataset.fold;
      if (collapsedKeys.has(k)) collapsedKeys.delete(k);
      else collapsedKeys.add(k);
      saveCollapsed();
      renderNav();
    };
  });
}

let groupCollapsed = false;
let savedCollapsed = null;
try {
  savedCollapsed = localStorage.getItem("skillmgr.collapsed");
} catch (_) {}
const collapsedKeys = new Set(savedCollapsed ? JSON.parse(savedCollapsed) : []);
let navInit = false;
let subDrag = null;

function saveCollapsed() {
  try {
    localStorage.setItem("skillmgr.collapsed", JSON.stringify([...collapsedKeys]));
  } catch (_) {}
}

function navSkillHtml(s, deep, extra) {
  const zh = zhOf(s);
  const label = zh || s.name;
  return `<div class="nav-skill${deep ? " deep" : ""}${extra || ""}" data-skill="${esc(s.name)}" title="${esc(s.name)}${zh ? " · " + esc(zh) : ""}">
      <span class="sk-dot"></span><span class="sk-t">${esc(label)}</span></div>`;
}

/* 在卡片页里定位并高亮某个技能；鼠标移上去后自动取消高亮 */
function focusSkillCard(name) {
  const card = document.querySelector(`.card[data-name="${CSS.escape(name)}"]`);
  if (!card) return false;
  document.querySelectorAll(".card.focus-flash").forEach((c) => c.classList.remove("focus-flash"));
  card.classList.add("focus-flash");
  card.scrollIntoView({ block: "center", behavior: "smooth" });
  card.addEventListener(
    "mouseenter",
    () => card.classList.remove("focus-flash"),
    { once: true }
  );
  return true;
}

function bindNavSkills(el) {
  el.querySelectorAll(".nav-skill").forEach((row) => {
    row.onclick = (e) => {
      e.stopPropagation();
      const name = row.dataset.skill;
      const s = STATE.skills.find((x) => x.name === name);
      if (!s) return;
      if (focusSkillCard(name)) return;
      // 不在当前视图：先切到它所在的分类，再定位
      current = s.group || "all";
      renderNav();
      render();
      focusSkillCard(name);
    };
  });
}

function renderNav() {
  if (!navInit) {
    navInit = true;
    if (savedCollapsed === null) {
      collapsedKeys.add("hub");
      collapsedKeys.add("global");
      STATE.roots.filter((r) => r.kind === "workspace").forEach((r) => collapsedKeys.add(r.key));
      saveCollapsed();
    }
  }
  const pin = document.getElementById("navPin");
  const nav = document.getElementById("nav");
  const items = navItems();
  const fixed = ["all", "hub"];
  const subs = items.filter((it) => it.sub);
  const workspaces = items.filter(
    (it) => !fixed.includes(it.key) && it.key !== "global" && !it.sub
  );
  const kids = (key) =>
    key === "all" || collapsedKeys.has(key) ? [] : STATE.skills.filter((s) => belongsTo(s, key));
  const withKids = (it, extra) =>
    navItemHtml(it, extra) + kids(it.key).map((s) => navSkillHtml(s, 0)).join("");
  const subBlock = (it) => {
    const gid = it.key.slice(3);
    const parent = it.parent || "global";
    const on = current === it.key ? " active" : "";
    const folded = collapsedKeys.has(it.key);
    return `<div class="nav-item nav-sub${on}" data-g="${esc(it.key)}" data-sgrow="${esc(gid)}" data-parent="${esc(parent)}" draggable="true" title="${esc(it.label)}">
          <span class="lbl"><button class="nav-fold${folded ? " collapsed" : ""}" data-fold="${esc(it.key)}" title="展开/收起">▸</button><button class="nav-del" data-sg="${esc(gid)}" title="删除这个分类">✕</button><span class="lbl-t">${esc(it.label)}</span></span>
          <span class="nav-right"><span class="cnt">${countOf(it.key)}</span><button class="nav-edit" data-rename="${esc(gid)}" title="重命名">✎</button></span>
        </div>` + kids(it.key).map((s) => navSkillHtml(s, 1)).join("");
  };
  const subsOf = (parent) => subs.filter((it) => (it.parent || "global") === parent);

  pin.innerHTML = items
    .filter((it) => fixed.includes(it.key))
    .map((it) => withKids(it, "") + subsOf(it.key).map(subBlock).join(""))
    .join("");

  nav.innerHTML =
    withKids(items.find((it) => it.key === "global"), " nav-primary") +
    subsOf("global").map(subBlock).join("") +
    (workspaces.length
      ? `<div class="nav-group${groupCollapsed ? " collapsed" : ""}" id="navGroup"><span class="ng-arrow">▸</span>${t("nav.workspaces")}</div>` +
        (groupCollapsed
          ? ""
          : workspaces
              .map(
                (it) =>
                  navItemHtml(it, " ws-item") +
                  kids(it.key).map((s) => navSkillHtml(s, 0, " ws-skill")).join("")
              )
              .join(""))
      : "");
  const foot = document.getElementById("navFoot");
  if (foot) {
    foot.innerHTML = `<div class="nav-item nav-trash${current === "trash" ? " active" : ""}" data-g="trash" title="回收站（可把卡片拖到这里删除）">
        <span class="lbl"><span class="lbl-t">${t("nav.trash")}</span><span class="cnt">${(STATE.trash || []).length}</span></span>
      </div>`;
    bindNavItems(foot);
    const trashNav = foot.querySelector("[data-g=\"trash\"]");
    if (trashNav) {
      trashNav.ondragover = (e) => {
        e.preventDefault();
        trashNav.classList.add("drop-hover");
        if (dragSkill) showDragTip("移入回收站", "松手即删除，10 天内可以恢复", true);
      };
      trashNav.ondragleave = () => trashNav.classList.remove("drop-hover");
      trashNav.ondrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        trashNav.classList.remove("drop-hover");
        hideDragTip();
        if (dragSkill) {
          const nm = dragSkill.name;
          dragSkill = null;
          doDeleteSkill(nm);
        }
      };
    }
  }
  bindNavItems(pin);
  bindNavItems(nav);
  bindNavSkills(pin);
  bindNavSkills(nav);
  [pin, nav].forEach((root) => {
    root.querySelectorAll("[data-sgrow]").forEach((row) => {
      row.ondragstart = (e) => {
        subDrag = { id: row.dataset.sgrow, parent: row.dataset.parent };
        try {
          e.dataTransfer.effectAllowed = "move";
        } catch (_) {}
      };
      row.ondragover = (e) => {
        e.preventDefault();
        if (subDrag) {
          if (subDrag.id === row.dataset.sgrow) return;
          row.classList.add("sub-hover");
          showDragTip("移动分类", "只改分类归属，不影响挂载", false);
          return;
        }
        row.classList.add("sub-hover");
        showDragTip(`归类到「${groupLabel(row.dataset.g)}」`, "只是查看分类，不影响挂载", false);
      };
      row.ondragleave = () => row.classList.remove("sub-hover");
      row.ondrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        row.classList.remove("sub-hover");
        hideDragTip();
        if (subDrag) {
          const moved = subDrag;
          subDrag = null;
          if (moved.parent === row.dataset.parent) reorderSub(moved.parent, moved.id, row.dataset.sgrow);
          else moveSub(moved.id, row.dataset.parent, row.dataset.sgrow);
          return;
        }
        if (dragSkill) assignToSub(dragSkill.name, row.dataset.sgrow);
      };
      row.ondragend = () => {
        subDrag = null;
        hideDragTip();
      };
    });
  });
  [pin, nav].forEach((root) =>
    root.querySelectorAll("[data-add]").forEach((b) => {
      b.onclick = (e) => {
        e.stopPropagation();
        openSubGroupDialog(b.dataset.add);
      };
    })
  );
  const asw = document.getElementById("agentSwitch");
  if (asw) {
    const lbl = document.getElementById("agentSwitchLabel");
    if (lbl) lbl.textContent = agentLabel();
    asw.onclick = (e) => {
      e.stopPropagation();
      openAgentPicker();
    };
  }
  const aset = document.getElementById("agentSettings");
  if (aset) {
    aset.onclick = (e) => {
      e.stopPropagation();
      openAgentSettings();
    };
  }
  const bl = document.getElementById("btnLang");
  if (bl) {
    bl.textContent = LANG === "en" ? "EN" : "中";
    bl.onclick = (e) => {
      e.stopPropagation();
      setLang(LANG === "en" ? "zh" : "en");
    };
  }
  const bh = document.getElementById("btnHelp");
  if (bh) {
    bh.onclick = (e) => {
      e.stopPropagation();
      showOnboarding();
    };
  }
  [pin, nav].forEach((root) =>
    root.querySelectorAll("[data-sg]").forEach((b) => {
      b.onclick = (e) => {
        e.stopPropagation();
        confirmRemoveSub(b.dataset.sg);
      };
    })
  );
  [pin, nav].forEach((root) =>
    root.querySelectorAll("[data-rename]").forEach((b) => {
      b.onclick = (e) => {
        e.stopPropagation();
        const gid = b.dataset.rename;
        const g = (STATE.config?.subGroups || []).find((x) => x.id === gid);
        if (g) openSubGroupDialog(g.parent || "global", { id: g.id, name: g.name, parent: g.parent || "global" });
      };
    })
  );
  const g = document.getElementById("navGroup");
  if (g) g.onclick = () => {
    groupCollapsed = !groupCollapsed;
    renderNav();
  };
}

/* ---------------- 子分类（纯查看用，不影响挂载） ---------------- */
function openSubGroupDialog(parent, edit) {
  if (document.getElementById("sgDialog")) return;
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const isEdit = !!(edit && edit.id);
  const p = isEdit ? (edit.parent || "global") : (parent === "hub" ? "hub" : "global");
  const pLabel = p === "hub" ? t("nav.hub") : t("nav.global");
  const box = document.createElement("div");
  box.id = "sgDialog";
  box.innerHTML = `
    <div class="overlay on" id="sgOverlay"></div>
    <div class="lp on" id="sgBox">
      <div class="lp-head">
        <div class="lp-badge">${isEdit ? "✎" : "＋"}</div>
        <div>
          <div class="lp-title">${isEdit ? t("sg.renameTitle") : t("sg.newTitle")}</div>
          <div class="lp-sub">${isEdit
            ? t("sg.renameSub")
            : t("sg.newSub", { p: pLabel })}</div>
        </div>
      </div>
      <div class="lp-body">
        <input id="sgName" class="sg-input" maxlength="24" placeholder="比如：前端、运维、文档" autocomplete="off">
      </div>
      <div class="lp-acts">
        <div class="btn ghost" id="sgCancel">${t("btn.cancel")}</div>
        <div class="btn primary" id="sgOk">${isEdit ? t("btn.save") : t("sg.create")}</div>
      </div>
    </div>`;
  document.body.appendChild(box);
  const input = box.querySelector("#sgName");
  if (isEdit) input.value = edit.name || "";
  const close = () => box.remove();
  const submit = async () => {
    const name = input.value.trim();
    if (!name) {
      input.focus();
      return;
    }
    try {
      if (isEdit) {
        const d = await api("/api/subgroup", {
          method: "POST",
          body: JSON.stringify({ action: "rename", id: edit.id, name }),
        });
        close();
        await refresh(d.state);
        showToast(t("tt.47"), `${edit.name} → ${name}`);
      } else {
        const d = await api("/api/subgroup", {
          method: "POST",
          body: JSON.stringify({ action: "add", name, parent: p }),
        });
        close();
        await refresh(d.state);
        showToast(t("tt.27"), `${name} → ${pLabel}`);
      }
    } catch (e) {
      showToast(isEdit ? "重命名失败" : "创建失败", e.message);
    }
  };
  box.querySelector("#sgOverlay").onclick = close;
  box.querySelector("#sgCancel").onclick = close;
  box.querySelector("#sgOk").onclick = submit;
  input.onkeydown = (e) => {
    if (e.key === "Enter") submit();
    if (e.key === "Escape") close();
  };
  setTimeout(() => input.focus(), 30);
}

function confirmRemoveSub(gid) {
  if (document.getElementById("sgDel")) return;
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const g = (STATE.config?.subGroups || []).find((x) => x.id === gid);
  const name = g ? g.name : "分类";
  const count = countOf("sg:" + gid);
  const pLabel = (g?.parent || "global") === "hub" ? "SKILL仓库" : "全局SKILL";
  const box = document.createElement("div");
  box.id = "sgDel";
  box.innerHTML = `
    <div class="overlay on" id="sdOverlay"></div>
    <div class="lp on" id="sdBox">
      <div class="lp-head">
        <div class="lp-badge">⚠</div>
        <div>
          <div class="lp-title">${t("sd.title")} <em>${esc(name)}</em></div>
          <div class="lp-sub">${count
            ? t("sub.delNote", { n: count, p: pLabel })
            : "这个分类里还没有技能。分类只是查看用，删除不影响任何挂载。"}</div>
        </div>
      </div>
      <div class="lp-acts">
        <div class="btn ghost" id="sdCancel">${t("btn.cancel")}</div>
        <div class="btn danger solid" id="sdOk">${t("sd.ok")}</div>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#sdOverlay").onclick = close;
  box.querySelector("#sdCancel").onclick = close;
  box.querySelector("#sdOk").onclick = () => {
    close();
    removeSubGroup(gid);
  };
}

async function removeSubGroup(gid) {
  const g = (STATE.config?.subGroups || []).find((x) => x.id === gid);
  const name = g ? g.name : "分类";
  try {
    const d = await api("/api/subgroup", { method: "POST", body: JSON.stringify({ action: "remove", id: gid }) });
    if (current === "sg:" + gid) current = "global";
    await refresh(d.state);
    showToast(t("tt.40"), `${name}${d.moved ? `，${d.moved} 个技能回到全局SKILL` : ""}`);
  } catch (e) {
    showToast(t("tt.16"), e.message);
  }
}

async function assignToSub(skill, gid) {
  try {
    const d = await api("/api/subgroup", {
      method: "POST",
      body: JSON.stringify({ action: "assign", skill, id: gid }),
    });
    await refresh(d.state);
    showToast(t("tt.35"), `${skill} → ${groupLabel("sg:" + gid)}`);
  } catch (e) {
    showToast(t("tt.9"), e.message);
  }
}

async function reorderSub(parent, srcId, dstId) {
  const list = (STATE.config?.subGroups || []).filter((g) => (g.parent || "global") === parent);
  const ids = list.map((g) => g.id);
  const from = ids.indexOf(srcId);
  const to = ids.indexOf(dstId);
  if (from < 0 || to < 0 || from === to) return;
  const [moved] = ids.splice(from, 1);
  ids.splice(to, 0, moved);
  try {
    const d = await api("/api/subgroup", {
      method: "POST",
      body: JSON.stringify({ action: "reorder", parent, ids }),
    });
    await refresh(d.state);
    showToast(t("tt.31"), groupLabel("sg:" + srcId));
  } catch (e) {
    showToast(t("tt.4"), e.message);
  }
}

async function moveSub(id, parent, before) {
  try {
    const d = await api("/api/subgroup", {
      method: "POST",
      body: JSON.stringify({ action: "move", id, parent, before: before || null }),
    });
    await refresh(d.state);
    showToast(t("tt.32"), `${groupLabel("sg:" + id)} → ${parent === "hub" ? "SKILL仓库" : "全局SKILL"}`);
  } catch (e) {
    showToast(t("tt.23"), e.message);
  }
}

function render() {
  if (current.startsWith("sg:") && !(STATE.config?.subGroups || []).some((g) => "sg:" + g.id === current)) {
    current = "global";
  } else if (
    current.startsWith("ws:") &&
    !STATE.roots.some((r) => r.key === current)
  ) {
    current = "global";
  }
  if (current === "trash") {
    renderTrash();
    return;
  }
  document.getElementById("viewTitle").textContent =
    current === "all" ? t("nav.all") : current === "hub" ? t("nav.hub") : current === "global" ? t("nav.global") : groupLabel(current);
  const list = STATE.skills.filter((s) => {
    if (!belongsTo(s, current)) return false;
    if (!query) return true;
    const q = query.toLowerCase();
    return (
      s.name.toLowerCase().includes(q) ||
      (s.nameZh || "").includes(query) ||
      (s.desc || "").toLowerCase().includes(q)
    );
  });
  list.sort((a, b) => {
    const pa = a.pinned ? 1 : 0, pb = b.pinned ? 1 : 0;
    if (pa !== pb) return pb - pa;
    if (sortBy === "time") return (b.mtime || 0) - (a.mtime || 0);
    if (sortBy === "size") return (b.sizeKb || 0) - (a.sizeKb || 0);
    return a.name.localeCompare(b.name);
  });
  document.getElementById("viewSub").textContent =
    `${t("badge.count", { n: list.length })} · ${t("badge.linkedN", { n: list.filter((s) => s.status === "linked").length })}`;

  const grid = document.getElementById("grid");
  if (!list.length) {
    grid.innerHTML = `<div class="empty">${t("empty.none")}</div>`;
    return;
  }
  grid.innerHTML = list
    .map((s, i) => {
      const g = groupOf(s);
      const links = (s.links || []).map((l) => `<span class="badge b-off">${esc(l.label)}</span>`).join("");
      const size = s.sizeKb ? `${s.sizeKb} KB` : `${s.files || 0} files`;
      const nm = esc(s.name);
      const zh = zhOf(s);
      let action = "";
      if (s.status === "local") action = `<span class="mini" data-adopt="${nm}">${t("btn.adopt")} hub</span>`;
      else if (s.status === "dead") action = `<span class="mini link" data-link="${nm}">${t("btn.link")}</span>`;
      else if (s.status === "unlinked") action = `<span class="mini link" data-link="${nm}">${t("btn.link")}</span>`;
      else if (s.status === "linked") action = `<span class="mini" data-unlink="${nm}">${t("btn.unlink")}</span>`;
      const del = s.status === "local" ? "" : `<span class="mini danger" data-del="${nm}">${t("btn.del")}</span>`;
      const clone =
        g === "hub"
          ? `<span class="mini" data-clone="${nm}" title="copy">${t("btn.clone")}</span>`
          : "";
      return `<div class="card glass" data-name="${nm}" style="animation:in .3s ${i * 0.03}s both">
        <span class="card-read" data-read="${nm}" title="read">${t("btn.read")}</span>
        <span class="card-copy" data-copy="${nm}" title="copy name">${t("btn.copyName")}</span>
        <span class="card-pin${s.pinned ? " pinned" : ""}" data-pin="${nm}" title="${t("act.pin")}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="${s.pinned ? "currentColor" : "none"}"
               stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 17v5"/>
            <path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/>
          </svg>
        </span>
        <div class="card-head">
          <div style="display:flex;gap:12px;align-items:flex-start">
            <div class="ico g-${esc(g)}">${esc((s.name || "?").slice(0, 1).toUpperCase())}</div>
            <h3>${nm}${zh ? `<span class="cn">${esc(zh)}</span>` : ""}</h3>
          </div>
        </div>
        <div class="desc">${esc(s.desc) || t("card.empty")}</div>
        <div class="badges">
          ${statusBadge(s)}
          ${(s.familyCount || 1) > 1 ? `<span class="badge b-count" title="copies">${t("badge.copies", { n: s.familyCount })}</span>` : ""}
          ${(s.links || []).length > 1 ? `<span class="badge b-count">${t("badge.instances", { n: s.links.length })}</span>` : ""}
          ${links}
          <span class="badge b-off">${size}</span>
        </div>
        <div class="card-foot">
          ${action || '<span class="mini">—</span>'}
          <span class="mini" data-edit="${nm}">${t("btn.edit")}</span>
          <span class="mini" data-hist="${nm}">${t("btn.hist")}</span>
          ${clone}
          ${del}
          <span class="mtime">${fmtTime(s.mtime)}</span>
        </div>
      </div>`;
    })
    .join("");

  grid.querySelectorAll(".card").forEach((el) => {
    const name = el.dataset.name;
    const sk = STATE.skills.find((x) => x.name === name);
    el.draggable = true;
    el.ondragstart = (e) => {
      dragSkill = sk;
      el.classList.add("dragging");
      showDragHint(false);
      showDragTip(`拖动 ${sk.name}`, "放到左侧分类上", false);
      e.dataTransfer.effectAllowed = "move";
      try { e.dataTransfer.setData("text/plain", name); } catch (_) {}
    };
    el.ondragend = () => {
      el.classList.remove("dragging");
      hideDragHint();
      hideDragTip();
    };
    el.onclick = (e) => {
      if (e.target.classList.contains("mini")) return;
      openDrawer(sk);
    };
  });
  grid.querySelectorAll("[data-adopt]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); adopt(el.dataset.adopt); };
  });
  grid.querySelectorAll("[data-link]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); linkTo(el.dataset.link, current); };
  });
  grid.querySelectorAll("[data-unlink]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); unlink(el.dataset.unlink); };
  });
  grid.querySelectorAll("[data-del]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); delSkill(el.dataset.del); };
  });
  grid.querySelectorAll("[data-clone]").forEach((el) => {
    el.onclick = async (e) => {
      e.stopPropagation();
      try {
        const d = await api("/api/skill/clone", {
          method: "POST",
          body: JSON.stringify({ name: el.dataset.clone }),
        });
        await refresh(d.state);
        showToast(t("tt.33"), `${d.from} → ${d.name}（内容相同，可挂到别的 agent）`);
      } catch (err) {
        showToast(t("tt.7"), err.message);
      }
    };
  });
  grid.querySelectorAll("[data-pin]").forEach((el) => {
    el.onmousedown = (e) => e.stopPropagation();
    el.onclick = async (e) => {
      e.stopPropagation();
      const s = STATE.skills.find((x) => x.name === el.dataset.pin);
      try {
        const d = await api("/api/pin", {
          method: "POST",
          body: JSON.stringify({ name: el.dataset.pin, pinned: !s.pinned }),
        });
        await refresh(d.state);
        showToast(s.pinned ? "已取消置顶" : "已置顶", el.dataset.pin);
      } catch (err) {
        showToast(t("tt.18"), err.message);
      }
    };
  });
  grid.querySelectorAll("[data-copy]").forEach((el) => {
    el.onmousedown = (e) => e.stopPropagation();
    el.onclick = async (e) => {
      e.stopPropagation();
      const nm = el.dataset.copy;
      try {
        await copyText(nm);
        showToast(t("tt.33"), nm);
      } catch (err) {
        showToast(t("tt.7"), err.message || "剪贴板不可用");
      }
    };
  });
  grid.querySelectorAll("[data-read]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); openReader(el.dataset.read); };
  });
  grid.querySelectorAll("[data-edit]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); openEditor(el.dataset.edit); };
  });
  grid.querySelectorAll("[data-hist]").forEach((el) => {
    el.onclick = (e) => { e.stopPropagation(); openHistoryFor(el.dataset.hist); };
  });
}

function renderPending() {
  const all = STATE.skills.filter((s) => s.status === "local");
  const box = document.getElementById("pending");
  if (!all.length || pendingDismissed) {
    box.classList.add("hide");
    return;
  }
  box.classList.remove("hide");
  document.getElementById("pendCount").textContent = all.length;
  document.getElementById("pendList").innerHTML = all
    .map((s) => `<div class="p-item">
      <span class="t">${esc(s.name)}<i>${esc(zhOf(s))}</i></span>
      <span class="p-btn" data-n="${esc(s.name)}">${t("pd.adopt")}</span>
    </div>`).join("");
  document.querySelectorAll(".p-btn").forEach((b) => (b.onclick = () => adopt(b.dataset.n)));
  const close = document.getElementById("pendClose");
  if (close) close.onclick = () => {
    pendingDismissed = true;
    try { localStorage.setItem("skillmgr.pendingHidden", "1"); } catch (_) {}
    renderPending();
  };
}

/* ---------------- 提示 ---------------- */
let toastTimer = null;
function showToast(title, msg) {
  document.getElementById("toastTitle").textContent = title;
  document.getElementById("toastMsg").textContent = msg;
  const el = document.getElementById("toast");
  el.classList.add("on");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("on"), 2800);
}

/* 技能目录支持热加载，挂载变化在新对话里生效；提示只做反馈，不假设特定客户端 */
function markRestartNeeded() {
  const el = document.getElementById("restartTip");
  if (el) el.classList.add("on");
}

/* 复制到剪贴板：优先 Clipboard API，失败退回 execCommand */
async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
  } catch (_) { /* 落到下面的兜底 */ }
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.cssText = "position:fixed;top:-1000px;left:-1000px;opacity:0";
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand("copy"); } finally { document.body.removeChild(ta); }
  if (!ok) throw new Error("剪贴板不可用");
}

/* ---------------- 接口 ---------------- */
async function api(path, opts) {
  const r = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...(opts || {}),
  });
  const data = await r.json().catch(() => ({}));
  if (!data.ok) throw new Error(data.error || "操作失败");
  return data;
}

async function refresh(state) {
  if (state) STATE = state;
  else STATE = await (await fetch("/api/state")).json();
  syncStats();
  renderNav();
  render();
  renderPending();
}

/* 重新扫一遍本地技能目录，并同步「已知名单」避免轮询重复提示 */
async function rescanSkills() {
  const btn = document.getElementById("btnRefresh");
  if (btn && btn.classList.contains("loading")) return;
  if (btn) btn.classList.add("loading");
  try {
    const st = await (await fetch("/api/rescan", { method: "POST" })).json();
    await refresh(st);
    knownNames = new Set(STATE.skills.map((s) => s.name));
    const linked = STATE.skills.filter((s) => s.status === "linked").length;
    showToast(t("tt.43"), `${t("badge.count", { n: STATE.skills.length })} · ${t("badge.linkedN", { n: linked })}`);
  } catch (e) {
    showToast(t("tt.19"), e.message);
  } finally {
    if (btn) btn.classList.remove("loading");
  }
}

function syncStats() {
  const linked = STATE.skills.filter((s) => s.status === "linked").length;
  document.getElementById("hubCount").textContent = STATE.skills.filter((s) => groupOf(s) === "hub" || s.status === "linked").length;
  document.getElementById("linkCount").textContent = linked;
  const foot = document.querySelector(".side-foot");
  if (!foot) return;
  if (STATE.hubPath) {
    foot.title = t("foot.title") + STATE.hubPath;
    const hp = foot.querySelector(".hub-path");
    if (hp) hp.textContent = "…" + STATE.hubPath.replace(/^.*?(\\data\\)/, "\\$1");
  }
  if (foot.dataset.bound) return;
  foot.dataset.bound = "1";
  foot.onclick = async () => {
    try {
      const d = await api("/api/reveal", {
        method: "POST",
        body: JSON.stringify({ path: STATE.hubPath || "" }),
      });
      showToast(t("tt.29"), d.path ? d.path.split(/[\\/]/).slice(-2).join("\\") : "data\\hub");
    } catch (e) {
      showToast(t("tt.1"), e.message);
    }
  };
}

async function adopt(name, target) {
  const s = STATE.skills.find((x) => x.name === name);
  const from = s ? s.group : "";
  try {
    const d = await api("/api/adopt", {
      method: "POST",
      body: JSON.stringify({ name, root: from, target: target || from }),
    });
    await refresh(d.state);
    showToast(t("tt.37"), target ? `${name} → ${groupLabel(target)}` : `${name} 已收纳进 hub`);
    markRestartNeeded();
  } catch (e) {
    showToast(t("tt.18"), e.message);
  }
}

async function linkTo(name, rootKey) {
  let target = rootKey;
  if (!target || target === "all" || target === "hub") {
    const s = STATE.skills.find((x) => x.name === name);
    target = s && s.lastRoot ? s.lastRoot : "";
  }
  if (!target) {
    showToast(t("tt.15"), "先在左侧选中要链接到的分类");
    return;
  }
  rootKey = target;
  try {
    const d = await api("/api/link", { method: "POST", body: JSON.stringify({ name, root: rootKey }) });
    await refresh(d.state);
    showToast(t("tt.37"), `${name} → ${groupLabel(rootKey)}`);
    markRestartNeeded();
  } catch (e) {
    showToast(t("tt.18"), e.message);
  }
}

async function unlink(name) {
  const s = STATE.skills.find((x) => x.name === name);
  const links = s?.links || [];
  if (!links.length) return;
  const targets = current === "all" || current === "hub"
    ? links
    : links.filter((l) => l.root === current);
  const list = targets.length ? targets : links;
  try {
    let st = null;
    for (const l of list) {
      const d = await api("/api/unlink", { method: "POST", body: JSON.stringify({ name, root: l.root }) });
      st = d.state;
    }
    if (st) await refresh(st);
    showToast(t("tt.39"), `${name} 仍在原分组，随时可重新链接`);
    markRestartNeeded();
  } catch (e) {
    showToast(t("tt.18"), e.message);
  }
}

function showLinkPicker(skill) {
  const links = skill.links || [];
  const box = document.createElement("div");
  box.innerHTML = `
    <div class="overlay on" id="lpOverlay"></div>
    <div class="lp on" id="lp">
      <div class="lp-head">
        <div class="lp-badge">⚠</div>
        <div>
          <div class="lp-title">${t("dlg.delTitle", { n: skill.name })}</div>
          <div class="lp-sub">${links.length > 1
            ? t("dlg.delSub", { n: links.length })
            : links.length === 1
              ? t("dlg.delSubOne", { g: links[0].label })
              : t("dlg.delSubNone")}</div>
        </div>
      </div>
      <div class="lp-body">
        <div class="lp-list">
          ${links.map((l) => `<label class="lp-item">
            <input type="checkbox" value="${esc(l.root)}">
            <span class="nm">${esc(l.label)}</span>
            <span class="pt">${esc(l.path || "")}</span>
          </label>`).join("")}
        </div>
        <div class="lp-note">${links.length
          ? `删除时会先移除全部 ${links.length} 处链接，技能移入回收站保留 ${STATE.trashDays || 10} 天。`
          : `技能会移入回收站保留 ${STATE.trashDays || 10} 天，期间可以恢复。`}</div>
        ${(skill.familyCount || 1) > 1
          ? `<label class="lp-fam"><input type="checkbox" id="lpFamily">
               <span>同时删除它的分身（共 ${skill.familyCount} 份，会合并成回收站里的一条）</span></label>`
          : ""}
      </div>
      <div class="lp-acts">
        <button class="btn ghost" id="lpCancel">${t("btn.cancel")}</button>
        ${links.length ? `<button class="btn danger" id="lpRemove">${t("dlg.delRemove")}</button>` : ""}
        <button class="btn danger solid" id="lpDelete">${t("dlg.delConfirm")}</button>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#lpCancel").onclick = close;
  box.querySelector("#lpOverlay").onclick = close;
  const removeBtn = box.querySelector("#lpRemove");
  if (removeBtn) removeBtn.onclick = async () => {
    const picked = [...box.querySelectorAll("input:checked")].map((i) => i.value);
    if (!picked.length) { showToast(t("tt.21"), "先勾选要移除的链接"); return; }
    try {
      let st = null;
      for (const root of picked) {
        const d = await api("/api/unlink", { method: "POST", body: JSON.stringify({ name: skill.name, root }) });
        st = d.state;
      }
      if (st) await refresh(st);
      close();
      showToast(t("tt.45"), `${skill.name} 移除了 ${picked.length} 处`);
    } catch (e) {
      showToast(t("tt.18"), e.message);
    }
  };
  box.querySelector("#lpDelete").onclick = async () => {
    const fam = box.querySelector("#lpFamily");
    const withFamily = !!(fam && fam.checked);
    close();
    await doDeleteSkill(skill.name, withFamily);
  };
}

function delSkill(name) {
  const s = STATE.skills.find((x) => x.name === name);
  if (!s) return;
  showLinkPicker(s);
}

async function doDeleteSkill(name, withFamily) {
  try {
    const d = await api("/api/skill", {
      method: "DELETE",
      body: JSON.stringify({ name, deleteFamily: !!withFamily }),
    });
    await refresh(d.state);
    const linkNote = d.removedLinks?.length ? `，已移除 ${d.removedLinks.length} 处链接` : "";
    const famNote = withFamily ? "（含分身，已合并为一条）" : "";
    showToast(t("tt.46"), `${name}${famNote}${linkNote} · ${STATE.trashDays || 10} 天后彻底删除`);
    markRestartNeeded();
  } catch (e) {
    showToast(t("tt.18"), e.message);
  }
}

/* ---------------- 工作区提示 ---------------- */
async function checkWorkspaces() {
  try {
    const w = await fetch("/api/workspaces").then((r) => r.json());
    const items = w.items || [];
    if (items.length) return;            // 已经认到工作区，不打扰
    if (w.parentExists && items.length) return;
    if (sessionStorage.getItem("wsPrompted") === "1") return;
    sessionStorage.setItem("wsPrompted", "1");
    showWorkspacePrompt(w.parent || "");
  } catch (_) {}
}

function showWorkspacePrompt(parent) {
  if (document.getElementById("wsPrompt")) return;
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const box = document.createElement("div");
  box.id = "wsPrompt";
  box.innerHTML = `
    <div class="overlay on" id="wpOverlay"></div>
    <div class="lp on" id="wpBox">
      <div class="lp-head">
        <div class="lp-badge">📁</div>
        <div>
          <div class="lp-title">${t("wp.title")}</div>
          <div class="lp-sub">软件在自己的目录（${esc(parent || "未设置")}）下没看到任何工作区。</div>
        </div>
      </div>
      <div class="lp-body">
        <div class="lp-note">${t("wp.note")}<br>
        选一个，软件会扫描它下面的每个子文件夹，里面只要有 <b>.dsh\skills</b> 就自动认成工作区。<br><br>
        也可以跳过——那样只会显示全局技能，之后随时能在设置（⚙）里改。</div>
      </div>
      <div class="lp-acts">
        <button class="btn ghost" id="wpSkip">${t("wp.skip")}</button>
        <button class="btn primary" id="wpPick">${t("wp.pick")}</button>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#wpOverlay").onclick = close;
  box.querySelector("#wpSkip").onclick = close;
  box.querySelector("#wpPick").onclick = async () => {
    try {
      if (!window.pywebview || !window.pywebview.api) {
        showToast(t("tt.22"), "请用桌面窗口模式，或在设置里手动填路径");
        return;
      }
      const dir = await window.pywebview.api.pick_folder();
      if (!dir) return;
      const d = await api("/api/workspace-parent", { method: "POST", body: JSON.stringify({ path: dir }) });
      STATE = d.state;
      current = "all";
      renderNav();
      render();
      renderPending();
      syncStats();
      close();
      const n = (STATE.roots || []).filter((r) => r.kind === "workspace").length;
      showToast(t("tt.41"), n ? `发现 ${n} 个工作区` : "这个目录下暂未发现工作区（子文件夹里要有 .dsh/skills）");
    } catch (e) {
      showToast(t("tt.17"), e.message);
    }
  };
}

/* ---------------- 分身同步询问 ---------------- */
function askFamilySync(n) {
  return new Promise((resolve) => {
    const box = document.createElement("div");
    box.innerHTML = `
      <div class="overlay on" id="fsOverlay"></div>
      <div class="lp on" id="fsBox">
        <div class="lp-head">
          <div class="lp-badge">⧉</div>
          <div>
            <div class="lp-title">${t("dlg.familySync")}</div>
            <div class="lp-sub">${t("dlg.familySyncSub", { n })}</div>
          </div>
        </div>
        <div class="lp-body">
          <div class="lp-note">· <b>同步</b>：所有分身一起改成新内容<br>
            · <b>${t("dlg.detachOnly")}</b>：它会断开和分身的关联，变成独立技能（名字保持不变）</div>
        </div>
        <div class="lp-acts">
          <button class="btn ghost" id="fsCancel">${t("btn.cancel")}</button>
          <button class="btn ghost" id="fsDetach">${t("dlg.detachOnly")}</button>
          <button class="btn primary" id="fsSync">${t("dlg.syncOnly")}</button>
        </div>
      </div>`;
    document.body.appendChild(box);
    const close = (v) => { box.remove(); resolve(v); };
    box.querySelector("#fsOverlay").onclick = () => close("cancel");
    box.querySelector("#fsCancel").onclick = () => close("cancel");
    box.querySelector("#fsSync").onclick = () => close("sync");
    box.querySelector("#fsDetach").onclick = () => close("detach");
  });
}

/* ---------------- 拖拽 ---------------- */
function onDrop(to, ev) {
  if (!dragSkill || to === "all") return;
  if (to.startsWith("sg:")) {
    assignToSub(dragSkill.name, to.slice(3));
    return;
  }
  if (groupOf(dragSkill) === to) return;
  const copy = !!(ev && ev.ctrlKey);
  // 目标位置已经挂了这个技能：直接提示，不弹确认
  if (!copy && (dragSkill.links || []).some((l) => l.root === to)) {
    showToast(t("tt.28"), `「${dragSkill.name}」已经挂在这个位置了`);
    return;
  }
  pendingMove = { skill: dragSkill, to, copy };
  const from = groupLabel(groupOf(dragSkill));
  const toLabel = groupLabel(to);
  let note;
  if (to === "hub") note = "移除所有链接，实体留在仓库";
  else if (copy) note = "复制：保留原链接，新增一处";
  else note = "移动：原位置的链接会被移除";
  document.getElementById("cbDesc").innerHTML =
    `<b>${esc(dragSkill.name)}</b> · ${esc(dragSkill.nameZh || "")}<br>` +
    `${esc(from)}<span class="cb-arrow">→</span><span class="cb-to">${esc(toLabel)}</span>` +
    `<span class="cb-note">${esc(note)}</span>`;
  document.getElementById("confirmbar").classList.add("on");
}

async function doMove() {
  if (!pendingMove) return;
  const { skill, to, copy } = pendingMove;
  pendingMove = null;
  document.getElementById("confirmbar").classList.remove("on");
  try {
    if (skill.status === "local") {
      await adopt(skill.name, to);
      return;
    }
    if (to === "hub") {
      const links = skill.links || [];
      let removed = 0, failed = 0;
      for (const l of links) {
        try {
          await api("/api/unlink", {
            method: "POST",
            body: JSON.stringify({ name: skill.name, root: l.root, toHub: true, purgeCopy: true }),
          });
          removed += 1;
        } catch (e) {
          failed += 1;
        }
      }
      const st = await (await fetch("/api/state")).json();
      await refresh(st);
      const msg = removed
        ? `${skill.name} 已回到仓库，移除了 ${removed} 处${failed ? `（${failed} 处失败）` : ""}`
        : `${skill.name} 已在仓库`;
      showToast(t("tt.42"), msg);
      markRestartNeeded();
      return;
    }
    if (!copy) {
      for (const l of skill.links || []) {
        if (l.root === to) continue;
        await api("/api/unlink", { method: "POST", body: JSON.stringify({ name: skill.name, root: l.root }) });
      }
    }
    const d = await api("/api/link", { method: "POST", body: JSON.stringify({ name: skill.name, root: to }) });
    await refresh(d.state);
    showToast(copy ? "已复制" : "已移动", `${skill.name} → ${groupLabel(to)}`);
    markRestartNeeded();
  } catch (e) {
    showToast(t("tt.18"), e.message);
  }
}

/* ---------------- 抽屉 ---------------- */
function openDrawer(s) {
  currentSkill = s;
  document.getElementById("dName").innerHTML = `${esc(s.name)}<span class="cn" style="margin-left:9px;font-size:12px;font-weight:400;color:var(--muted)">${esc(s.nameZh || "")}</span>`;
  document.getElementById("dDesc").textContent = s.desc || "（无描述）";
  document.getElementById("drawer").classList.add("on");
  document.getElementById("overlay").classList.add("on");
  setTab("overview", s);
}

function setTab(tab, s) {
  const skill = s || currentSkill;
  if (!skill) return;
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("on", t.dataset.tab === tab));
  const body = document.getElementById("dBody");
  if (tab === "overview") {
    body.innerHTML = `
      <dl class="kv">
        <dt>分类</dt><dd>${groupLabel(groupOf(skill))}</dd>
        <dt>状态</dt><dd>${skill.status === "linked" ? "已链接" : skill.status === "local" ? "待纳管" : skill.status === "dead" ? "死链" : "未链接"}</dd>
        <dt>链接位置</dt><dd>${(skill.links || []).map((l) => l.label).join("、") || "—"}</dd>
        <dt>体积</dt><dd>${skill.sizeKb} KB · ${skill.files} 个文件</dd>
        <dt>路径</dt><dd>${skill.path || "—"}</dd>
      </dl>
      <div class="section-t">SKILL.md 摘要</div>
      <div class="code">name: ${skill.name}
description: ${(skill.desc || "").slice(0, 160)}${(skill.desc || "").length > 160 ? "..." : ""}</div>`;
  } else if (tab === "links") {
    body.innerHTML = `
      <div class="section-t">${t("ln.current")}</div>
      ${(skill.links || []).map((l) => `<div class="link-row"><span>${l.label} · ${l.path}</span><span class="ghost" data-unlink-root="${l.root}">${t("btn.unlink")}</span></div>`).join("") || '<div class="link-row"><span>${t("ln.notLinked")}</span></div>'}
      <div class="section-t" style="margin-top:18px">${t("ln.canLink")}</div>
      ${STATE.roots.filter((r) => r.kind !== "hub").map((r) => `<div class="link-row"><span>${r.label}</span><span class="ghost" data-link-root="${r.key}">${t("btn.link")}</span></div>`).join("")}`;
    body.querySelectorAll("[data-unlink-root]").forEach((el) => {
      el.onclick = async () => {
        const d = await api("/api/unlink", { method: "POST", body: JSON.stringify({ name: skill.name, root: el.dataset.unlinkRoot }) });
        await refresh(d.state);
        showToast(t("tt.39"), skill.name);
        closeDrawer();
      };
    });
    body.querySelectorAll("[data-link-root]").forEach((el) => {
      el.onclick = async () => {
        const d = await api("/api/link", { method: "POST", body: JSON.stringify({ name: skill.name, root: el.dataset.linkRoot }) });
        await refresh(d.state);
        showToast(t("tt.37"), skill.name);
        closeDrawer();
      };
    });
  } else {
    body.innerHTML = `<div class="section-t">git 历史</div><div class="log">` +
      (STATE.history || []).map((h) => `<div class="log-item"><span class="t">${h.time}</span><span class="m">${h.message}</span></div>`).join("") +
      `</div>`;
  }
}

function closeDrawer() {
  document.getElementById("drawer").classList.remove("on");
  document.getElementById("overlay").classList.remove("on");
}




function openCreate() {
  const box = document.createElement("div");
  box.innerHTML = `
    <div class="overlay on" id="ncOverlay"></div>
    <div class="lp on" id="nc">
      <div class="lp-head">
        <div class="lp-badge" style="background:linear-gradient(135deg,rgba(124,108,240,.28),rgba(124,108,240,.10));border-color:rgba(124,108,240,.35)">＋</div>
        <div>
          <div class="lp-title">${t("nc.title")}</div>
          <div class="lp-sub">${t("nc.sub")}<span style="display:none">，SKILL.md 会按标准结构生成（何时使用 / 怎么做 / 示例 / 注意事项），之后拖到分类即可用。</div>
        </div>
      </div>
      <div class="lp-body" style="padding-bottom:0">
        <div class="nc-field"><label>${t("nc.name")}</label><input id="ncName" placeholder="my-skill" autocomplete="off"></div>
        <div class="nc-field"><label>${t("nc.zh")}</label><input id="ncZh" placeholder="${t("nc.phZh")}" autocomplete="off"></div>
        <div class="nc-field"><label>${t("nc.desc")}</label><input id="ncDesc" placeholder="${t("nc.phDesc")}" autocomplete="off"></div>
        <div class="nc-error" id="ncErr"></div>
      </div>
      <div class="lp-acts">
        <button class="btn ghost" id="ncCancel">${t("btn.cancel")}</button>
        <button class="btn" id="ncOk">${t("nc.createOnly")}</button>
        <button class="btn danger solid" id="ncCreateEdit" style="background:linear-gradient(135deg,#6d5ce0,#8b7bf0);box-shadow:0 6px 20px rgba(124,108,240,.3)">${t("nc.createEdit")}</button>
      </div>
    </div>`;
  document.body.appendChild(box);
  const close = () => box.remove();
  box.querySelector("#ncCancel").onclick = close;
  box.querySelector("#ncOverlay").onclick = close;
  const nameInput = box.querySelector("#ncName");
  nameInput.addEventListener("input", () => {
    // 只做大小写和空格处理，非法字符留给提交时提示，避免把用户输入静默吃掉
    const v = nameInput.value.replace(/\s+/g, "-").toLowerCase();
    if (v !== nameInput.value) nameInput.value = v;
  });
  const errBox = box.querySelector("#ncErr");
  const showErr = (msg) => {
    errBox.textContent = msg;
    errBox.classList.add("on");
  };
  const hideErr = () => errBox.classList.remove("on");

  box.querySelectorAll("input").forEach((el) => el.addEventListener("input", hideErr));
  nameInput.focus();

  const doCreate = async (thenEdit) => {
    hideErr();
    const name = box.querySelector("#ncName").value.trim();
    const zh = box.querySelector("#ncZh").value.trim();
    const desc = box.querySelector("#ncDesc").value.trim();
    if (!name) { showErr("先填名称"); return; }
    if (/[\u4e00-\u9fa5]/.test(name)) {
      showErr("名称只能用英文小写；中文名请填到下一栏");
      return;
    }
    if (!/^[a-z0-9][a-z0-9-]{1,63}$/.test(name)) {
      showErr("名称只能小写字母、数字、连字符，2-64 位");
      return;
    }
    try {
      const d = await api("/api/skill/create", {
        method: "POST",
        body: JSON.stringify({ name, name_zh: zh, description: desc }),
      });
      await refresh(d.state);
      close();
      current = "hub";
      renderNav();
      render();
      showToast(t("tt.26"), `${name} 在 SKILL仓库 里`);
      if (thenEdit) openEditor(name);
    } catch (e) {
      showErr(e.message);
    }
  };

  box.querySelector("#ncOk").onclick = () => doCreate(false);
  box.querySelector("#ncCreateEdit").onclick = () => doCreate(true);
}

/* ---------------- 拖动提示 ---------------- */
let hintEl = null;
function ensureHint() {
  if (hintEl) return hintEl;
  hintEl = document.createElement("div");
  hintEl.className = "drag-hint";
  hintEl.id = "dragHint";
  document.body.appendChild(hintEl);
  return hintEl;
}
function showDragHint(copyMode) {
  const el = ensureHint();
  el.innerHTML = copyMode
    ? '<b>松开鼠标 = 复制</b><span class="sep">|</span>原位置的链接会保留'
    : '拖到左侧分类来移动<span class="sep">|</span>按住 <b>Ctrl</b> 拖动 = 复制';
  el.classList.add("on");
}
function hideDragHint() {
  if (hintEl) hintEl.classList.remove("on");
}


/* ---------------- 编辑与按技能历史 ---------------- */
/* ---------------- 只读阅读 ---------------- */
function splitFrontmatter(md) {
  const m = String(md || "").match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { meta: {}, body: String(md || "") };
  const meta = {};
  m[1].split(/\r?\n/).forEach((line) => {
    const kv = line.match(/^([A-Za-z_][\w-]*)\s*:\s*(.*)$/);
    if (kv) meta[kv[1]] = kv[2].replace(/^["']|["']$/g, "");
  });
  return { meta, body: String(md || "").slice(m[0].length) };
}

function mdInline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
}

function mdToHtml(md) {
  const lines = String(md || "").split(/\r?\n/);
  const out = [];
  let inCode = false;
  const code = [];
  let inList = false;
  let tableRows = [];
  const flushTable = () => {
    if (!tableRows.length) return;
    const rows = tableRows.filter((r) => !/^\s*\|?[\s:|-]+\|?\s*$/.test(r));
    const cells = (r) =>
      r.replace(/^\s*\|/, "").replace(/\|\s*$/, "").split("|").map((c) => c.trim());
    if (rows.length) {
      const head = cells(rows[0]);
      const body = rows.slice(1);
      out.push(
        `<table><thead><tr>${head.map((c) => `<th>${mdInline(c)}</th>`).join("")}</tr></thead><tbody>` +
          body.map((r) => `<tr>${cells(r).map((c) => `<td>${mdInline(c)}</td>`).join("")}</tr>`).join("") +
          "</tbody></table>"
      );
    }
    tableRows = [];
  };
  const closeList = () => {
    if (inList) {
      out.push("</ul>");
      inList = false;
    }
  };
  for (const raw of lines) {
    if (/^\s*```/.test(raw)) {
      closeList();
      if (inCode) {
        out.push(`<pre><code>${esc(code.join("\n"))}</code></pre>`);
        code.length = 0;
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      code.push(raw);
      continue;
    }
    if (/^\s*\|.*\|/.test(raw)) {
      closeList();
      tableRows.push(raw);
      continue;
    }
    if (tableRows.length) flushTable();
    if (/^\s*$/.test(raw)) {
      closeList();
      continue;
    }
    const h = raw.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      closeList();
      const lv = h[1].length;
      out.push(`<h${lv}>${mdInline(h[2])}</h${lv}>`);
      continue;
    }
    const li = raw.match(/^\s*[-*]\s+(.*)$/);
    if (li) {
      if (!inList) {
        out.push("<ul>");
        inList = true;
      }
      out.push(`<li>${mdInline(li[1])}</li>`);
      continue;
    }
    const ol = raw.match(/^\s*(\d+)\.\s+(.*)$/);
    if (ol) {
      closeList();
      out.push(`<p class="ol"><b>${ol[1]}.</b> ${mdInline(ol[2])}</p>`);
      continue;
    }
    const q = raw.match(/^>\s?(.*)$/);
    if (q) {
      closeList();
      out.push(`<blockquote>${mdInline(q[1])}</blockquote>`);
      continue;
    }
    const hr = raw.match(/^\s*(---+|\*\*\*+)\s*$/);
    if (hr) {
      closeList();
      out.push("<hr>");
      continue;
    }
    closeList();
    out.push(`<p>${mdInline(raw)}</p>`);
  }
  if (inCode && code.length) out.push(`<pre><code>${esc(code.join("\n"))}</code></pre>`);
  flushTable();
  closeList();
  return out.join("");
}

async function openReader(name) {
  if (document.getElementById("rd")) return;
  const s = STATE.skills.find((x) => x.name === name);
  let content = "";
  try {
    const r = await fetch("/api/skill/content?name=" + encodeURIComponent(name));
    const d = await r.json();
    if (!d.ok) throw new Error(d.error || "读取失败");
    content = d.content;
  } catch (e) {
    showToast(t("tt.5"), e.message);
    return;
  }
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const sizeTxt = s && s.sizeKb ? `${s.sizeKb} KB` : "";
  const timeTxt = s && s.mtime ? fmtTime(s.mtime) : "";
  const { meta, body } = splitFrontmatter(content);
  const metaRows = Object.entries(meta)
    .map(([k, v]) => `<div class="rd-kv"><span>${esc(k)}</span><b>${esc(v)}</b></div>`)
    .join("");
  const box = document.createElement("div");
  box.id = "rdBox";
  box.innerHTML = `
    <div class="rd-overlay on" id="rdOverlay"></div>
    <div class="rd on" id="rd">
      <div class="rd-head">
        <div class="rd-h-l">
          <div class="rd-title">${esc(s?.name || name)}${s?.nameZh ? `<span class="cn">${esc(s.nameZh)}</span>` : ""}</div>
          <div class="rd-sub">${[esc(name) + "/SKILL.md", sizeTxt, timeTxt].filter(Boolean).join(" · ")}</div>
        </div>
        <div class="rd-acts">
          <span class="mini" id="rdCopy">${t("rd.copyAll")}</span>
          <span class="mini" id="rdCopyPath">${t("rd.copyPath")}</span>
          <div class="x" id="rdClose">✕</div>
        </div>
      </div>
      <div class="rd-body" id="rdBody">${metaRows ? `<div class="rd-meta">${metaRows}</div>` : ""}${mdToHtml(body)}</div>
      <div class="rd-foot"><span class="rd-hint">${t("rd.readonly")}</span></div>
    </div>`;
  document.body.appendChild(box);
  const close = () => {
    document.removeEventListener("keydown", onKey, true);
    box.remove();
  };
  const onKey = (e) => {
    if (e.key === "Escape") {
      e.stopPropagation();
      close();
    }
  };
  document.addEventListener("keydown", onKey, true);
  box.querySelector("#rdOverlay").onclick = close;
  box.querySelector("#rdClose").onclick = close;
  document.getElementById("rdBody").scrollTop = 0;
  box.querySelector("#rdCopy").onclick = async () => {
    await copyText(content);
    showToast(t("tt.33"), `${name}/SKILL.md 全文`);
  };
  box.querySelector("#rdCopyPath").onclick = async () => {
    await copyText(s?.path || name);
    showToast(t("tt.33"), s?.path || name);
  };
}

async function openEditor(name) {
  const s = STATE.skills.find((x) => x.name === name);
  let content = "";
  try {
    const r = await fetch("/api/skill/content?name=" + encodeURIComponent(name));
    const d = await r.json();
    if (!d.ok) throw new Error(d.error || "读取失败");
    content = d.content;
  } catch (e) {
    showToast(t("tt.5"), e.message);
    return;
  }

  const box = document.createElement("div");
  box.innerHTML = `
    <div class="ed-overlay" id="edOverlay"></div>
    <div class="ed-modal" id="edModal">
      <div class="ed-head">
        <span class="ed-title">${name}/SKILL.md</span>
        <span class="ed-sub">${t("rd.gitNote")}</span>
        <span class="ed-close" id="edClose">✕</span>
      </div>
      <textarea id="edText" spellcheck="false"></textarea>
      <div class="ed-foot">
        <span class="ed-hint">Ctrl + S 保存</span>
        <button class="btn" id="edCancel">${t("btn.cancel")}</button>
        <button class="btn primary" id="edSave">${t("rd.saveCommit")}</button>
      </div>
    </div>`;
  document.body.appendChild(box);

  const ta = box.querySelector("#edText");
  ta.value = content;
  ta.scrollTop = 0;
  ta.setSelectionRange(0, 0);

  const close = () => box.remove();
  const save = async (andClose) => {
    try {
      const cur = STATE.skills.find((x) => x.name === name);
      let syncFamily = false;
      let detachFamily = false;
      if (cur && (cur.familyCount || 1) > 1) {
        const n = cur.familyCount - 1;
        const choice = await askFamilySync(n);
        if (choice === "cancel") return;
        if (choice === "sync") syncFamily = true;
        if (choice === "detach") detachFamily = true;
      }
      const d = await api("/api/skill/content", {
        method: "PUT",
        body: JSON.stringify({ name, content: ta.value, syncFamily, detachFamily }),
      });
      await refresh(d.state);
      const updated = STATE.skills.find((x) => x.name === name);
      if (updated && document.getElementById("drawer")?.classList.contains("on") && currentSkill?.name === name) {
        openDrawer(updated);
      }
      let syncNote = "";
      if (d.synced && d.synced.length) syncNote = `，已同步到 ${d.synced.length} 个分身`;
      if (d.detached) syncNote = "，已断开和分身的关联，现在是独立技能";
      showToast(t("tt.24"), `${name}/SKILL.md 已提交${syncNote}`);
      if (andClose) close();
    } catch (e) {
      showToast(t("tt.0"), e.message);
    }
  };

  box.querySelector("#edClose").onclick = close;
  box.querySelector("#edCancel").onclick = close;
  box.querySelector("#edOverlay").onclick = close;
  box.querySelector("#edSave").onclick = () => save(true);
  ta.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
      e.preventDefault();
      save(false);
    }
    if (e.key === "Escape") close();
  });
  ta.focus();
}

function openHistoryFor(name) {
  const s = STATE.skills.find((x) => x.name === name);
  currentSkill = s;
  document.getElementById("dName").innerHTML = `历史 <span class="cn" style="font-size:12px;color:var(--muted)">${esc(name)}</span>`;
  document.getElementById("dDesc").textContent = "与该技能相关的提交记录";
  document.getElementById("drawer").classList.add("on");
  document.getElementById("overlay").classList.add("on");
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("on", t.dataset.tab === "history"));
  const rows = (STATE.history || []).filter((h) => h.message.includes(name));
  const body = document.getElementById("dBody");
  body.innerHTML = rows.length
    ? `<div class="log">` + rows.map((h) =>
        `<div class="log-item"><span class="t">${h.time}</span><span class="m">${h.message}</span></div>`
      ).join("") + `</div>`
    : `<div class="empty">${t("empty.noHist")}</div>`;
}

/* ---------------- 历史与导入 ---------------- */
function openHistory() {
  currentSkill = null;
  document.getElementById("dName").innerHTML = "操作历史";
  document.getElementById("dDesc").textContent = "每次纳管、链接、删除都会自动提交到 hub 的 git 仓库";
  document.getElementById("drawer").classList.add("on");
  document.getElementById("overlay").classList.add("on");
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("on", t.dataset.tab === "history"));
  const body = document.getElementById("dBody");
  const rows = STATE.history || [];
  body.innerHTML = rows.length
    ? `<div class="log">` + rows.map((h) =>
        `<div class="log-item"><span class="t">${h.time}</span><span class="m">${h.message}</span></div>`
      ).join("") + `</div>`
    : `<div class="empty">${t("empty.noHist")}</div>`;
}

async function importSkill() {
  try {
    if (!window.pywebview || !window.pywebview.api) {
      showToast(t("tt.2"), "请用桌面窗口模式打开");
      return;
    }
    const dir = await window.pywebview.api.pick_folder();
    if (!dir) return;
    const d = await api("/api/import", { method: "POST", body: JSON.stringify({ path: dir }) });
    await refresh(d.state);
    showToast(t("tt.30"), "技能已收进 SKILL仓库");
  } catch (e) {
    showToast(t("tt.3"), e.message);
  }
}

/* ---------------- 自动发现新技能 ---------------- */
let knownNames = new Set();

function watchNewSkills() {
  setInterval(async () => {
    try {
      const st = await (await fetch("/api/state")).json();
      if (!st || !st.skills) return;
      const names = new Set(st.skills.map((s) => s.name));
      const added = [...names].filter((n) => !knownNames.has(n));
      const removed = [...knownNames].filter((n) => !names.has(n));
      if (!added.length && !removed.length) return;
      STATE = st;
      knownNames = names;
      renderNav();
      render();
      renderPending();
      syncStats();
      if (added.length) {
        pendingDismissed = false;
        try { localStorage.removeItem("skillmgr.pendingHidden"); } catch (_) {}
        const fresh = st.skills.filter((s) => added.includes(s.name) && s.status === "local");
        showToast(t("tt.6"), fresh.length
          ? `${fresh.map((s) => s.name).join("、")} 待纳管`
          : added.join("、"));
      }
    } catch (e) {
      /* 忽略轮询错误 */
    }
  }, 45000);
}

/* ---------------- 侧栏宽度拖拽 ---------------- */
function initResizer() {
  const shell = document.querySelector(".shell");
  const rz = document.getElementById("navResizer");
  if (!shell || !rz) return;
  const MIN = 240, MAX = 620, DEF = 300;
  let w = DEF;
  try {
    const v = parseInt(sessionStorage.getItem("skillmgr.navWidth") || "", 10);
    if (v) w = v;
  } catch (_) {}
  const apply = (v) => {
    const max = Math.max(MIN, Math.min(MAX, window.innerWidth - 420));
    w = Math.round(Math.max(MIN, Math.min(v, max)));
    shell.style.gridTemplateColumns = w + "px 1fr";
    rz.style.left = w + "px";
    return w;
  };
  apply(w);
  let dragging = false;
  let startX = 0;
  let startW = 0;
  rz.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragging = true;
    startX = e.clientX;
    startW = w;
    rz.classList.add("on");
    try {
      rz.setPointerCapture(e.pointerId);
    } catch (_) {}
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  });
  rz.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    e.preventDefault();
    apply(startW + (e.clientX - startX));
  });
  const endDrag = (e) => {
    if (!dragging) return;
    dragging = false;
    rz.classList.remove("on");
    try {
      rz.releasePointerCapture(e.pointerId);
    } catch (_) {}
    document.body.style.cursor = "";
    document.body.style.userSelect = "";
    try {
      sessionStorage.setItem("skillmgr.navWidth", String(w));
    } catch (_) {}
  };
  rz.addEventListener("pointerup", endDrag);
  rz.addEventListener("pointercancel", endDrag);
  rz.addEventListener("dblclick", () => {
    apply(DEF);
    try {
      sessionStorage.setItem("skillmgr.navWidth", String(DEF));
    } catch (_) {}
  });
  window.addEventListener("resize", () => apply(w));
}

/* ---------------- 首次使用说明 ---------------- */
/* ---------------- 功能导览（聚光灯式） ---------------- */
function tourSteps() {
  return [
    {
      sel: null,
      t: "先花一分钟认识它",
      d: "技能文件只存一份。要它在某个地方生效，就在那里放一个快捷方式指过去；暂时不用的，就留在「SKILL仓库」里。\n注意：「SKILL仓库」是一个分类，专门放未挂载（暂时不用）的技能，需要你自己把卡片拖进去；「全局SKILL」和各工作区放已挂载的。三处看到的是同一批文件，只是视角不同。下面按顺序过一遍。",
      hint: "建议先看完（约 1 分钟），右上角的 ? 随时能重新打开这份教程。\n跳过也没关系：左下角会一直列出「待纳管」的技能，点「纳入」就能逐个收进来；点顶部的「刷新」会重新扫描，发现你后来放进去的技能。",
      en: {"t": "One minute intro", "d": "A skill file exists once. To use it somewhere, put a shortcut pointing back to it; unused ones simply stay in the SKILL Hub.\nNote: the Hub is a category for unlinked (unused) skills — you drag cards in yourself. Global and workspaces hold the linked ones. All three views show the same files from different angles.", "hint": "Watching to the end takes ~1 minute; the ? button reopens this guide anytime.\nSkipping is fine: pending skills stay listed at the bottom-left and you can adopt them one by one; Refresh rescans to pick up skills you add later."},
    },
    {
      sel: ".search",
      t: "搜索",
      d: "在当前分类里按名称、中文名或描述过滤。\n只影响显示，不动任何文件、也不改挂载。",
      en: {"t": "Search", "d": "Filters the current category by name, Chinese name, or description.\nDisplay only — it never touches files or links."},
    },
    {
      sel: ".agent-bar",
      t: "切换 Agent · 设置",
      d: "每个 agent（DSH / Claude Code / Codex…）有自己的全局目录和工作区挂载点，但**共用同一个 SKILL仓库**——技能真身只有一份。\n左边切换当前看的是哪一个；右边齿轮打开设置，可以勾选管理哪些、改它们的目录。",
      en: {"t": "Switch agent · Settings", "d": "Each agent (DeepSeek / Claude Code / Codex…) has its own global dir and workspace mount points, but they all share one SKILL Hub — the file exists once.\nSwitch the current one on the left; the gear on the right opens settings to pick agents and edit their paths."},
    },
    {
      sel: "#navPin .nav-item[data-g=\"all\"]",
      t: "全部",
      d: "当前 agent 下所有技能的总览，包括已挂载的和躺在仓库里没挂的。\n点这里只是换个查看范围。",
      en: {"t": "All", "d": "Everything under the current agent, linked or not.\nJust a different view."},
    },
    {
      sel: "#navPin .nav-item[data-g=\"hub\"]",
      t: "SKILL仓库（公用）",
      d: "这是「暂时不用」的存放处，只放未挂载的技能——放在这里就等于暂时不用，所有 agent 都看不到它。\n所有 agent 共用这一个仓库。一个技能默认只有一份；想拆成几份分别给不同 agent 用（各改各的、互不影响），用卡片上的「复制」做分身。\n想把技能移动到这里，需要你自己把卡片拖进来：拖进来的那一刻会自动取消它在所有位置的挂载（技能本身不删，只是撤下）。想重新启用，再拖回去即可。",
      en: {"t": "SKILL Hub (shared)", "d": "Where skills you don't currently use sit — only unlinked ones live here, so no agent can see them.\nAll agents share this hub. A skill exists once by default; use Copy on a card to fork it for different agents.\nYou drag cards in yourself: that moment removes its links everywhere (the skill itself is kept, just unmounted). Drag it back to re-enable."},
    },
    {
      sel: "#nav .nav-item[data-g=\"global\"]",
      t: "全局SKILL",
      d: "挂到这里的技能，对所有项目都生效。\n把卡片拖进来 = 建立挂载；拖出去 = 取消。一个技能可以同时挂多处，改一处全部生效。\n按住 Ctrl 拖动 = 复制到别的分区，让它在两处同时挂载（原挂载保留，不移动）。\n也可以直接点卡片上的「链接 / 取消链接」来挂载或停止挂载，不必拖拽。",
      en: {"t": "Global", "d": "Skills here apply to every project.\nDrag a card in = link it; drag out = unlink. One skill can be linked in many places and edits propagate.\nHold Ctrl while dragging = copy into another section so both stay linked (the original link is kept).\nYou can also click Link / Unlink on the card instead of dragging."},
    },
    {
      sel: '[data-add="global"]',
      t: "新建子分类",
      d: "仓库和全局SKILL 行右侧的 ＋ 可以新建子分类，比如「前端」「运维」。\n子分类只是查看用的分组，不影响挂载——归到哪一类，和它在哪生效是两回事。\n拖卡片到子分类 = 归类；行上的 ✎ 改名，✕ 删除（里面的技能会回到母分类，不会被删）。子分类之间还能拖动排序。",
      en: {"t": "Create a group", "d": "The ＋ on the Hub and Global rows creates a sub-group (e.g. frontend, ops).\nGroups are display-only — grouping a skill does not change where it is linked.\nDrag a card onto a group to file it; ✎ renames, ✕ deletes (skills return to the parent, nothing is deleted). Groups can be dragged to reorder."},
    },
    {
      sel: "#navGroup",
      t: t("nav.workspaces"),
      d: "每个工作区是一个独立的挂载点，挂进来只对这个工作区生效。\n同一个技能可以按住 Ctrl 拖动，复制到其他工作区，两边同时挂载。\n检测范围：只看工作区母文件夹里的 skills，工作区内按项目分的子文件夹一律不扫（那些技能请单独管理）。",
      en: {"t": "Workspaces", "d": "Each workspace is an independent mount point; linking here only affects that workspace.\nHold Ctrl while dragging to copy the skill into another workspace so both stay linked.\nDetection scope: only the workspace root's skills folder is scanned — any per-project subfolder is intentionally ignored."},
    },
    {
      sel: "#navFoot",
      t: "回收站",
      d: "删掉的技能先到这里，保留 10 天，期间随时能恢复。\n注意：拖卡片进来 = 删除，会先切断它在所有位置的链接，再整份移进回收站；10 天后文件本体真的被删掉。\n如果以后可能还用，别删——把它拖进「SKILL仓库」暂存就行（只是撤下挂载，文件不删）。",
      en: {"t": "Trash", "d": "Deleted skills land here for 10 days and can be restored anytime.\nNote: dropping a card here = delete — its links are cut first, then the whole folder moves to trash; after 10 days the files are really gone.\nIf you might need it later, don't delete: drop it into the SKILL Hub instead (unmounts only)."},
    },
    {
      sel: ".card",
      t: "技能卡片",
      d: "一张卡就是一个技能：名称、中文名、描述、状态徽章、挂载位置、大小、最后修改时间。\n状态分四种：已链接、未链接（在仓库）、待纳管（工作区里还没进仓库）、死链。",
      en: {"t": "Skill card", "d": "One card = one skill: name, Chinese name, description, status badge, link locations, size, last modified.\nFour states: Linked, In hub, Pending (in a workspace, not adopted yet), Broken link."},
    },
    {
      sel: ".card .card-foot",
      t: "卡片操作",
      d: "链接 / 取消链接、编辑、历史、删除。\n主操作（链接）用主题色高亮；删除是红的，点了先进回收站，不会立刻消失。",
      en: {"t": "Card actions", "d": "Link / Unlink, Edit, History, Delete.\nThe primary action is highlighted; Delete is red and moves to trash rather than removing instantly."},
    },
    {
      sel: ".card",
      t: "鼠标拖动",
      d: "拖卡片到全局或某个工作区 = 移动挂载（原位置撤下，新位置挂上）。\n按住 Ctrl 拖 = 复制，两处同时挂载。\n拖到 SKILL仓库 = 撤下所有挂载、暂存起来；拖到回收站 = 删除（先断链，再整份进回收站）。\n拖动过程中屏幕中间会实时提示「松手会发生什么」。",
      en: {"t": "Drag & drop", "d": "Drag a card to Global or a workspace = move the link (removed here, added there).\nHold Ctrl = copy, linked in both places.\nDrop on SKILL Hub = unlink everything and park it; drop on Trash = delete (unlink first).\nWhile dragging, the hint in the middle tells you what will happen on release."},
    },
    {
      sel: ".card",
      t: "复制一个分身",
      d: "仓库里每张卡片都有「复制」按钮：点一下就会多出一个一模一样的技能（名字自动加 -2）。\n用途是把同一个技能拆成两份，分别挂给不同的 agent，各自改各自的，互不影响。\n有分身时卡片上会标「共 N 份」；删除时会问你「是否连分身一起删」，一起删的话回收站里只占一条，恢复时只回来一个（等于取消分身）。",
      en: {"t": "Make a copy", "d": "Every card in the Hub has a Copy button: it creates an identical skill (name gets -2 appended).\nUse it to split one skill into two, each linked to a different agent, edited independently.\nCards show \"N copies\"; deleting asks whether to remove all copies — if so, trash holds one entry and restoring brings back a single skill (the copies are dropped)."},
    },
    {
      sel: ".card",
      t: "卡片右上角",
      d: "鼠标移到卡片上，右上角出现「阅读」和「复制」。\n阅读是只读渲染 SKILL.md（还能复制全文或路径），不会改动文件；复制只是复制技能名。",
      en: {"t": "Top-right of a card", "d": "Hover a card to reveal Read and Copy.\nRead renders SKILL.md read-only (and can copy the full text or path) without modifying anything; Copy only copies the skill name."},
    },
    {
      sel: ".actions",
      t: "顶部操作",
      d: "排序（名称/修改时间/大小）、刷新扫描、查看全部历史、新建技能、导入已有目录。\n新建和导入只是把技能放进 SKILL仓库，不会自动挂载。",
      en: {"t": "Toolbar", "d": "Sort (name / modified / size), rescan, view full history, create a skill, import an existing folder.\nCreating or importing only puts the skill in the Hub — nothing is linked automatically."},
    },
    {
      sel: ".tb-right",
      t: "顶栏右侧",
      d: "? 随时重开这份导览，◐ 切换主题，后面是最小化 / 最大化 / 关闭。\n主题选择会记住，下次打开还是这个。",
      en: {"t": "Top-right buttons", "d": "? reopens this guide, ◐ switches theme, followed by minimize / maximize / close.\nThe theme choice is remembered."},
    },
    {
      sel: null,
      t: "让 agent 也能操作",
      d: "界面上的事都有命令行版本，agent（包括给你干活的那些）可以直接调用，不用点鼠标。\n18 条命令：list / get / create / update / link / unlink / delete / restore / history / diff / rollback / recover / validate / audit 等；默认输出 JSON，写操作要 --yes，支持 --dry-run 先看会做什么。\n入口是 cli\\skill.py（Windows 另有 skill.cmd 包装），你只要说一句「用 skill 命令帮我把某技能挂到某个工作区」，它就能做。",
      en: {"t": "Agents can drive it too", "d": "Everything the UI does has a CLI equivalent, so agents (including the ones working for you) can call it without clicking.\n18 commands: list / get / create / update / link / unlink / delete / restore / history / diff / rollback / recover / validate / audit and more; JSON by default, writes need --yes, and --dry-run previews changes.\nEntry point: cli\\skill.py (plus a skill.cmd wrapper on Windows). Just say \"use the skill command to link X into workspace Y\"."},
    },
    {
      sel: null,
      t: "关于「纳管」",
      d: "工作区里已经存在的技能，需要先纳管：程序会复制到统一存放处 → 校验 → 删原目录 → 在原位置建链接，任何一步失败都会回滚。\n注意：纳管不是把技能放进「SKILL仓库」分类，而是把文件搬到软件管理的目录里；两者不是一回事。\n这一步只在你点下面的按钮时执行；之后它不会自己动任何文件。",
      final: true,
      en: {"t": "About adoption", "d": "Skills that already exist in a workspace must be adopted first: copy into the store → verify → remove the original → create a link in place. Any failure rolls back.\nNote: adoption is not the same as putting a skill into the SKILL Hub — it moves the files into the managed store.\nIt only runs when you press the button below; afterwards it never touches files on its own."},
    },
  ];
}

function showOnboarding() {
  if (document.getElementById("tour")) return;
  const pending = (STATE.skills || []).filter((s) => s.status === "local");
  const toast = document.getElementById("toast");
  if (toast) toast.classList.remove("on");
  const steps = tourSteps();
  let idx = 0;

  const root = document.createElement("div");
  root.id = "tour";
  root.innerHTML = `
    <div class="tour-mask" id="tMaskTop"></div>
    <div class="tour-mask" id="tMaskBottom"></div>
    <div class="tour-mask" id="tMaskLeft"></div>
    <div class="tour-mask" id="tMaskRight"></div>
    <div class="tour-hole" id="tHole"></div>
    <div class="tour-card" id="tCard">
      <div class="tour-step" id="tStep"></div>
      <div class="tour-t" id="tTitle"></div>
      <div class="tour-d" id="tDesc"></div>
      <div class="tour-hint" id="tHint"></div>
      <div class="tour-acts">
        <button class="btn ghost" id="tSkip">${t("btn.skip")}</button>
        <div class="tour-nav">
          <button class="btn ghost" id="tPrev">${t("btn.prev")}</button>
          <button class="btn primary" id="tNext">${t("btn.next")}</button>
        </div>
      </div>
    </div>`;
  document.body.appendChild(root);

  const masks = {
    top: root.querySelector("#tMaskTop"),
    bottom: root.querySelector("#tMaskBottom"),
    left: root.querySelector("#tMaskLeft"),
    right: root.querySelector("#tMaskRight"),
  };
  const hole = root.querySelector("#tHole");
  const card = root.querySelector("#tCard");

  function place(step) {
    const el = step.sel ? document.querySelector(step.sel) : null;
    const W = window.innerWidth;
    const H = window.innerHeight;
    if (el) {
      el.scrollIntoView({ block: "nearest", behavior: "smooth" });
      const r = el.getBoundingClientRect();
      const pad = 6;
      const x = Math.max(0, r.left - pad);
      const y = Math.max(0, r.top - pad);
      const w = r.width + pad * 2;
      const h = r.height + pad * 2;
      hole.style.display = "block";
      hole.style.left = x + "px";
      hole.style.top = y + "px";
      hole.style.width = w + "px";
      hole.style.height = h + "px";
      masks.top.style.cssText = `display:block;left:0;top:0;width:${W}px;height:${y}px`;
      masks.bottom.style.cssText = `display:block;left:0;top:${y + h}px;width:${W}px;height:${Math.max(0, H - y - h)}px`;
      masks.left.style.cssText = `display:block;left:0;top:${y}px;width:${x}px;height:${h}px`;
      masks.right.style.cssText = `display:block;left:${x + w}px;top:${y}px;width:${Math.max(0, W - x - w)}px;height:${h}px`;

      // 卡片定位：优先下方，其次上方，最后居中
      const cw = 380;
      const ch = card.offsetHeight || 190;
      let cx = Math.min(Math.max(14, r.left + r.width / 2 - cw / 2), W - cw - 14);
      let cy = y + h + 14;
      if (cy + ch > H - 14) {
        if (y - ch - 14 > 14) cy = y - ch - 14;
        else cy = Math.max(14, (H - ch) / 2);
      }
      card.style.left = cx + "px";
      card.style.top = cy + "px";
    } else {
      hole.style.display = "none";
      Object.values(masks).forEach((m) => (m.style.display = "block"));
      masks.top.style.cssText = `display:block;left:0;top:0;width:${W}px;height:${H}px`;
      masks.bottom.style.cssText = "display:none";
      masks.left.style.cssText = "display:none";
      masks.right.style.cssText = "display:none";
      const cw = 400;
      card.style.left = (W - cw) / 2 + "px";
      card.style.top = Math.max(40, (H - (card.offsetHeight || 190)) / 2) + "px";
      card.style.width = cw + "px";
      return;
    }
    card.style.width = "380px";
  }

  function sync() {
    const step = steps[idx];
    root.querySelector("#tStep").textContent = `${idx + 1} / ${steps.length}`;
    const L = LANG === "en" && step.en ? step.en : null;
    root.querySelector("#tTitle").textContent = L ? L.t : step.t;
    root.querySelector("#tDesc").textContent = L ? L.d : step.d;
    const hintEl = root.querySelector("#tHint");
    const hintText = LANG === "en" && step.en && step.en.hint ? step.en.hint : step.hint;
    if (hintText) {
      hintEl.textContent = hintText;
      hintEl.style.display = "block";
    } else {
      hintEl.style.display = "none";
    }
    root.querySelector("#tPrev").disabled = idx === 0;
    const next = root.querySelector("#tNext");
    if (step.final) {
      next.textContent = pending.length ? `${t("btn.adoptN", { n: pending.length })}` : t("btn.start");
    } else {
      next.textContent = t("btn.next");
    }
    place(step);
    requestAnimationFrame(() => place(step));
  }

  root.querySelector("#tPrev").onclick = () => {
    if (idx > 0) {
      idx -= 1;
      sync();
    }
  };
  root.querySelector("#tNext").onclick = () => {
    if (idx < steps.length - 1) {
      idx += 1;
      sync();
      return;
    }
    finish(true);
  };
  root.querySelector("#tSkip").onclick = () => finish(false);
  window.addEventListener("resize", () => sync());

  async function finish(doAdopt) {
    root.remove();
    window.removeEventListener("resize", sync);
    try {
      const cand = await fetch("/api/agents/candidates").then((r) => r.json());
      const detected = (cand.items || []).filter((i) => i.detected).map((i) => ({ ...i, enabled: true }));
      if (detected.length) {
        const d = await api("/api/agents/save", { method: "POST", body: JSON.stringify({ items: detected }) });
        if (d.state) STATE = d.state;
        renderNav();
        syncStats();
      }
    } catch (_) {}
    if (doAdopt && pending.length) {
      try {
        const d = await api("/api/adopt-all", { method: "POST", body: "{}" });
        if (d.state) {
          STATE = d.state;
          renderNav();
          render();
          renderPending();
          syncStats();
        }
        const failed = (d.results || []).filter((r) => !r.ok);
        if (failed.length) {
          showToast(t("tt.11"), `成功 ${d.adopted}/${d.total}，失败：${failed.map((f) => f.name).join("、")}`);
        } else {
          showToast(t("tt.13"), `${t("tt.adoptedN", { n: d.total })}`);
        }
      } catch (e) {
        showToast(t("tt.12"), e.message);
      }
    }
    try {
      const d2 = await api("/api/onboard", { method: "POST", body: "{}" });
      if (d2.state) STATE = d2.state;
    } catch (_) {}
  }

  sync();
}

/* ---------------- 启动 ---------------- */
(async function init() {
  const st = await (await fetch("/api/state")).json();
  STATE = st;
  knownNames = new Set(st.skills.map((s) => s.name));
  curTheme = st.config.theme || "black";
  if (!THEMES.includes(curTheme)) curTheme = "black";
  setTheme(curTheme);

  applyI18n();
  syncStats();
  renderNav();
  render();
  renderPending();
  initResizer();
  if (!st.config.onboarded) {
    showOnboarding();
  } else {
    setTimeout(checkWorkspaces, 800);
  }

  document.getElementById("q").oninput = (e) => {
    query = e.target.value.trim();
    render();
  };
  document.querySelectorAll(".tab").forEach((t) => (t.onclick = () => setTab(t.dataset.tab)));
  document.getElementById("dClose").onclick = closeDrawer;
  document.getElementById("overlay").onclick = closeDrawer;
  document.getElementById("btnTheme").onclick = openThemePicker;
  document.getElementById("cbCancel").onclick = () => {
    pendingMove = null;
    document.getElementById("confirmbar").classList.remove("on");
  };
  document.getElementById("cbOk").onclick = doMove;

  const api = () => window.pywebview && window.pywebview.api;
  const bindWin = (id, fn) => {
    const el = document.getElementById(id);
    if (el) el.onclick = () => { try { api() && api()[fn](); } catch (e) {} };
  };
  bindWin("btnMin", "minimize");
  bindWin("btnMax", "toggle_max");
  bindWin("btnClose", "close");



  const bh = document.getElementById("btnHistory");
  if (bh) bh.onclick = openHistory;
  const bi = document.getElementById("btnImport");
  if (bi) bi.onclick = importSkill;
  const bc = document.getElementById("btnCreate");
  if (bc) bc.onclick = openCreate;
  const br = document.getElementById("btnRefresh");
  if (br) br.onclick = rescanSkills;
  const sortSel = document.getElementById("sortBy");
  if (sortSel) {
    sortSel.value = sortBy;
    sortSel.onchange = () => {
      sortBy = sortSel.value;
      try { localStorage.setItem("skillmgr.sort", sortBy); } catch (_) {}
      render();
    };
  }
  const rt = document.getElementById("restartTip");
  if (rt) rt.onclick = () => rt.classList.remove("on");

  const bar = document.querySelector(".titlebar");
  if (bar) {
    bar.addEventListener("mousedown", async (e) => {
      if (e.button !== 0) return;
      if (e.target.closest(".win-btn")) return;
      const apiRef = window.pywebview && window.pywebview.api;
      if (!apiRef) return;
      let base;
      try {
        base = await apiRef.get_pos();
      } catch (err) {
        return;
      }
      const ox = e.screenX - base[0];
      const oy = e.screenY - base[1];
      let raf = null;
      let last = null;
      const onMove = (ev) => {
        last = ev;
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = null;
          if (!last) return;
          apiRef.move_to(last.screenX - ox, last.screenY - oy);
        });
      };
      const onUp = () => {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
        if (raf) cancelAnimationFrame(raf);
      };
      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
    });
  }

  document.addEventListener("dragover", (e) => {
    if (!dragSkill) return;
    e.preventDefault();
    showDragHint(!!e.ctrlKey);
  });
  document.addEventListener("drop", () => {
    hideDragHint();
  });

  watchNewSkills();
})();
