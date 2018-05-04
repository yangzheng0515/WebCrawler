#100offer_crawler
## 100offer招聘信息采集 
入口页/列表页：https://cn.100offer.com/job_positions
内容页：https://cn.100offer.com/job_positions/11890

列表页采集内容：职位ID、职位URL、是否推荐
内容页采集内容：职位名称 公司名称 薪资 工作经验要求 学历要求 教育经历要求 城市
             上次活跃时间 技能要求 公司福利 职位介绍 工作地点 URL 职位ID


需要注意的是，获取登录页面的随机参数和登录时提交表单，要使用同一个session，如果不是同一个session，获取的参数与提交表单是的参数不一致，导致验证不通过

