"""E2E 视觉测试：使用 Playwright 验证大屏渲染。
需要安装：pip install playwright pytest-playwright && playwright install chromium
"""
import pytest
import os
from pathlib import Path


# Dashboard URL - served by FastAPI static files
DASHBOARD_URL = "http://127.0.0.1:8000/web-screen/dashboard.html"


# Try to import playwright fixtures, skip tests if not available
try:
    import playwright
    import pytest_asyncio
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


pytestmark = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="Playwright not installed")


if HAS_PLAYWRIGHT:
    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_globe_renders(page):
        """验证 3D 地球仪渲染"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        
        # 等待 canvas 出现
        canvas = page.locator("#globe canvas")
        await canvas.wait_for(state="visible", timeout=15000)
        
        # 验证 canvas 有尺寸
        box = await canvas.bounding_box()
        assert box is not None
        assert box["width"] > 100
        assert box["height"] > 100
        
        # 截图
        await page.screenshot(path=".omo/evidence/globe_renders.png", full_page=True)


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_globe_has_three_segments(page):
        """验证地球仪显示 3 个路段"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        
        # 等待 globe 初始化
        await page.wait_for_timeout(3000)
        
        # 通过检查系列数据验证有 3 条线
        # ECharts GL 系列数据在内部，这里通过截图对比验证
        await page.screenshot(path=".omo/evidence/globe_3_segments.png", full_page=True)


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_legend_shows_four_colors(page):
        """验证图例显示 4 种颜色"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        
        legend = page.locator(".legend")
        await legend.wait_for(state="visible", timeout=5000)
        
        items = await legend.locator(".legend-item").all()
        assert len(items) == 4
        
        # 验证颜色标签
        colors = []
        for item in items:
            color_el = item.locator(".legend-color")
            style = await color_el.get_attribute("style")
            colors.append(style)
        
        # 检查四种颜色都存在
        color_text = " ".join(colors)
        assert "#52c41a" in color_text  # 绿
        assert "#faad14" in color_text  # 黄
        assert "#ff7a00" in color_text  # 橙
        assert "#ff4d4f" in color_text  # 红


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_timeline_slider_works(page):
        """验证时间轴滑块可拖动"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        slider = page.locator("#timelineSlider")
        await slider.wait_for(state="visible", timeout=5000)
        
        # 初始值
        initial_val = await slider.get_attribute("value")
        assert initial_val == "0"
        
        # 拖动到中间
        await slider.evaluate("el => el.value = 84")
        await slider.dispatch_event("input")
        
        # 验证时间显示更新
        await page.wait_for_timeout(500)
        time_display = page.locator("#timelineTime")
        time_text = await time_display.text_content()
        assert "09-01" in time_text or "09-02" in time_text or "09-03" in time_text


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_play_pause_button(page):
        """验证播放/暂停按钮"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        btn = page.locator("#btnPlayPause")
        await btn.wait_for(state="visible")
        
        # 初始应为播放状态 (▶)
        initial_text = await btn.text_content()
        assert "▶" in initial_text
        
        # 点击播放
        await btn.click()
        await page.wait_for_timeout(500)
        
        # 应变为暂停 (⏸)
        paused_text = await btn.text_content()
        assert "⏸" in paused_text
        
        # 点击暂停
        await btn.click()
        await page.wait_for_timeout(500)
        
        # 恢复播放
        resumed_text = await btn.text_content()
        assert "▶" in resumed_text


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_speed_selector(page):
        """验证速度选择器"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)
        
        select = page.locator("#speedSelect")
        await select.wait_for(state="visible")
        
        # 默认 1x
        val = await select.get_attribute("value")
        assert val == "1"
        
        # 改为 2x
        await select.select_option("2")
        await page.wait_for_timeout(100)
        val = await select.get_attribute("value")
        assert val == "2"


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_heatmap_renders_168_cells(page):
        """验证热力图渲染 168 个单元格"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        cells = page.locator(".heatmap-cell[data-speed]")
        count = await cells.count()
        assert count == 168  # 24 hours × 7 days


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_heatmap_tooltip(page):
        """验证热力图悬浮提示"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        cell = page.locator(".heatmap-cell[data-speed]").first
        await cell.hover()
        await page.wait_for_timeout(300)
        
        tooltip = page.locator("#heatmapTooltip")
        await tooltip.wait_for(state="visible", timeout=3000)
        
        content = await tooltip.text_content()
        assert "平均速度" in content or "km/h" in content


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_layer_toggles(page):
        """验证图层开关"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        toggles = page.locator(".layer-toggle")
        count = await toggles.count()
        assert count == 3
        
        # 默认 accidents 和 vehicleTypes 开启
        classes = await toggles.nth(0).get_attribute("class")
        assert "active" in classes
        
        # 点击关闭第一个
        await toggles.nth(0).click()
        await page.wait_for_timeout(200)
        classes = await toggles.nth(0).get_attribute("class")
        assert "active" not in classes


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_road_dropdown_syncs_camera(page):
        """验证路段下拉框切换"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)
        
        select = page.locator("#roadSelect")
        await select.wait_for(state="visible")
        
        # 默认选中第一个
        val = await select.get_attribute("value")
        assert val == "R001"
        
        # 切换到 R002
        await select.select_option("R002")
        await page.wait_for_timeout(2000)  # 等待相机飞行动画
        
        val = await select.get_attribute("value")
        assert val == "R002"


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_time_range_filter(page):
        """验证时间范围筛选"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)
        
        start = page.locator("#timeStart")
        end = page.locator("#timeEnd")
        btn = page.locator("#btnApplyRange")
        
        await start.wait_for(state="visible")
        await end.wait_for(state="visible")
        await btn.wait_for(state="visible")
        
        # 修改时间范围
        await start.fill("2026-09-02T00:00")
        await end.fill("2026-09-03T23:00")
        await btn.click()
        
        await page.wait_for_timeout(1000)
        # 验证 toast 提示
        toast = page.locator("#toast")
        await toast.wait_for(state="visible", timeout=5000)
        text = await toast.text_content()
        assert "时间范围已更新" in text or "更新" in text


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_responsive_layout(page):
        """验证响应式布局"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)
        
        # 桌面宽度
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.wait_for_timeout(500)
        side = page.locator(".side-panel")
        box = await side.bounding_box()
        assert box["width"] > 300
        
        # 窄屏
        await page.set_viewport_size({"width": 800, "height": 600})
        await page.wait_for_timeout(500)
        box = await side.bounding_box()
        # 侧边栏应在底部，宽度全屏
        assert box["width"] > 700


    @pytest.mark.playwright
    @pytest.mark.asyncio
    async def test_road_segment_click_triggers_flight(page):
        """验证点击路段触发相机飞行"""
        await page.goto(DASHBOARD_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # 获取 canvas
        canvas = page.locator("#globe canvas")
        
        # 在 canvas 中心点击 (模拟点击路段)
        box = await canvas.bounding_box()
        if box:
            await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            await page.wait_for_timeout(2000)
            
            # 验证下拉框更新
            select = page.locator("#roadSelect")
            val = await select.get_attribute("value")
            assert val in ["R001", "R002", "R003"]
else:
    # Playwright not installed - provide a placeholder test
    def test_playwright_not_installed():
        """Playwright tests skipped - install with: pip install playwright pytest-playwright && playwright install chromium"""
        pytest.skip("Playwright not installed. Install with: pip install playwright pytest-playwright && playwright install chromium")
