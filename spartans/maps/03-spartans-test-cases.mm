<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="SPARTANS 测试用例脑图">
    <node TEXT="登录与权限" POSITION="right">
      <node TEXT="邮箱密码登录">
        <node TEXT="正确凭证"/>
        <node TEXT="错误密码和禁用账号"/>
      </node>
      <node TEXT="邮箱验证码">
        <node TEXT="正确、错误、过期"/>
        <node TEXT="重发与频控"/>
      </node>
      <node TEXT="角色权限">
        <node TEXT="未申请、审核中、拒绝、通过管理者"/>
        <node TEXT="订阅用户与机器人虚拟账户"/>
      </node>
      <node TEXT="越权">
        <node TEXT="控制台路由和他人机器人"/>
        <node TEXT="私域白名单"/>
        <node TEXT="现货直链和 API 权限"/>
      </node>
    </node>
    <node TEXT="策略市集" POSITION="right">
      <node TEXT="默认列表">
        <node TEXT="每页 12 条、3 列、总数与页码"/>
      </node>
      <node TEXT="周期">
        <node TEXT="7 天、30 天默认、90 天"/>
        <node TEXT="卡片统计口径同步"/>
      </node>
      <node TEXT="排序">
        <node TEXT="收益率、AUM、订阅人数、胜率"/>
        <node TEXT="相同值稳定排序"/>
      </node>
      <node TEXT="搜索">
        <node TEXT="完整、部分、大小写和空结果"/>
        <node TEXT="特殊字符与防注入"/>
      </node>
      <node TEXT="组合条件">
        <node TEXT="周期、排序、搜索、分页组合"/>
        <node TEXT="条件变化回第一页"/>
      </node>
      <node TEXT="五分钟数据更新"/>
    </node>
    <node TEXT="机器人详情与订阅资格" POSITION="right">
      <node TEXT="状态">
        <node TEXT="战斗中、暂停、下架、无仓位"/>
      </node>
      <node TEXT="指标">
        <node TEXT="ROI、MDD、净值、夏普、胜率、AUM"/>
      </node>
      <node TEXT="交易信息">
        <node TEXT="当前持仓、等待信号和历史订单"/>
        <node TEXT="手续费与资金费"/>
      </node>
      <node TEXT="资格">
        <node TEXT="公域"/>
        <node TEXT="私域 UID 白名单"/>
        <node TEXT="合伙人白名单"/>
        <node TEXT="AUM 已达上限"/>
      </node>
    </node>
    <node TEXT="订阅" POSITION="right">
      <node TEXT="表单校验">
        <node TEXT="空金额、最小值、超过余额、MAX"/>
        <node TEXT="小数精度和舍入"/>
      </node>
      <node TEXT="风险披露">
        <node TEXT="未勾选不可提交"/>
        <node TEXT="勾选后可提交"/>
      </node>
      <node TEXT="批次处理">
        <node TEXT="整点前、整点边界和批次后提交"/>
        <node TEXT="重复提交和批次前取消"/>
      </node>
      <node TEXT="份额计算">
        <node TEXT="净值小于、等于、大于 1"/>
        <node TEXT="包含未实现盈亏"/>
        <node TEXT="币种与份额精度"/>
      </node>
      <node TEXT="资金一致性">
        <node TEXT="用户余额、资金账户、总份额和 AUM"/>
        <node TEXT="操作记录"/>
      </node>
      <node TEXT="失败回滚">
        <node TEXT="余额变化、机器人暂停和 AUM 超限"/>
        <node TEXT="批次任务失败"/>
      </node>
    </node>
    <node TEXT="追加资金" POSITION="right">
      <node TEXT="仅限已订阅机器人"/>
      <node TEXT="复用首次订阅校验和批次规则"/>
      <node TEXT="新份额按当前净值计算"/>
      <node TEXT="原份额、总份额和操作记录正确"/>
    </node>
    <node TEXT="统一资金池" POSITION="right">
      <node TEXT="净值公式">
        <node TEXT="总资产除以总份额"/>
        <node TEXT="零份额初始化与负收益"/>
        <node TEXT="手续费和资金费计入"/>
      </node>
      <node TEXT="用户权益">
        <node TEXT="多用户不同份额"/>
        <node TEXT="盈利亏损按比例分配"/>
        <node TEXT="用户权益之和等于池权益"/>
      </node>
      <node TEXT="资金划转">
        <node TEXT="资金到账合约"/>
        <node TEXT="合约到账资金"/>
        <node TEXT="API、手动和失败场景"/>
      </node>
      <node TEXT="并发">
        <node TEXT="订阅与交易同时发生"/>
        <node TEXT="赎回与平仓同时发生"/>
        <node TEXT="多用户同批次"/>
      </node>
    </node>
    <node TEXT="赎回" POSITION="left">
      <node TEXT="表单">
        <node TEXT="空金额、超过可赎回、部分和 MAX"/>
        <node TEXT="重复请求"/>
      </node>
      <node TEXT="净值与份额">
        <node TEXT="包含未实现盈亏"/>
        <node TEXT="提交到处理间净值变化"/>
        <node TEXT="份额扣减和到账精度"/>
      </node>
      <node TEXT="全部平仓">
        <node TEXT="流动性充足和全部用户可赎回"/>
      </node>
      <node TEXT="每小时队列">
        <node TEXT="当前请求可满足"/>
        <node TEXT="大额不可满足时检查后续小额"/>
        <node TEXT="补充流动性后重试"/>
        <node TEXT="顺序与公平性"/>
      </node>
      <node TEXT="状态">
        <node TEXT="已提交、排队中、处理中"/>
        <node TEXT="成功、部分成功、取消、失败退回"/>
      </node>
      <node TEXT="对账">
        <node TEXT="用户份额、资金账户、AUM、用户余额"/>
        <node TEXT="操作记录一致"/>
      </node>
    </node>
    <node TEXT="赎回超时风控" POSITION="left">
      <node TEXT="每小时邮件">
        <node TEXT="频次、内容和重复抑制"/>
      </node>
      <node TEXT="超过 5 天">
        <node TEXT="Lark 每日通知运营与 BD"/>
      </node>
      <node TEXT="超过 7 天">
        <node TEXT="强制介入权限"/>
        <node TEXT="暂停、强平、自动赎回和下架"/>
        <node TEXT="延期与每日跟踪"/>
      </node>
      <node TEXT="异常">
        <node TEXT="联系不到管理者"/>
        <node TEXT="通知、划转或清算失败"/>
      </node>
    </node>
    <node TEXT="管理者申请与审核" POSITION="left">
      <node TEXT="首次申请">
        <node TEXT="必填项、格式和重复提交"/>
      </node>
      <node TEXT="状态">
        <node TEXT="未申请、审核中、通过和拒绝"/>
      </node>
      <node TEXT="拒绝重申">
        <node TEXT="拒绝原因与原详情"/>
        <node TEXT="重新编辑提交"/>
      </node>
      <node TEXT="运营审核">
        <node TEXT="权限、审核记录和并发审核"/>
      </node>
    </node>
    <node TEXT="创建机器人" POSITION="left">
      <node TEXT="公域与私域"/>
      <node TEXT="名称">
        <node TEXT="英文数字、禁止空格和 25 字符边界"/>
        <node TEXT="重名"/>
      </node>
      <node TEXT="标签与说明">
        <node TEXT="风险标签、策略标签和数量上限"/>
        <node TEXT="富文本必填、超长和安全"/>
      </node>
      <node TEXT="资料审核">
        <node TEXT="审核中、通过、拒绝"/>
        <node TEXT="未审核不可公开"/>
      </node>
      <node TEXT="Tier 限制">
        <node TEXT="Bot Limit 和 AUM 上限"/>
      </node>
    </node>
    <node TEXT="机器人账户与 API" POSITION="left">
      <node TEXT="虚拟账户">
        <node TEXT="获取密码、验证码和身份验证器前置"/>
        <node TEXT="重置密码"/>
      </node>
      <node TEXT="交易权限">
        <node TEXT="仅开放合约"/>
        <node TEXT="现货直链不可访问"/>
      </node>
      <node TEXT="API 凭证">
        <node TEXT="默认掩码、查看二次验证和复制"/>
        <node TEXT="轮换与吊销"/>
      </node>
      <node TEXT="API 交易">
        <node TEXT="下单、撤单、平仓和账户划转"/>
        <node TEXT="签名、权限和限频"/>
      </node>
    </node>
    <node TEXT="Tier 等级" POSITION="left">
      <node TEXT="条件边界">
        <node TEXT="自有资金、ROI、MDD、赎回时效和交易量"/>
        <node TEXT="无违规硬条件"/>
      </node>
      <node TEXT="升级">
        <node TEXT="投入资金即时判断"/>
        <node TEXT="每日 UTC+0 和等于阈值"/>
      </node>
      <node TEXT="降级">
        <node TEXT="每周一分润后"/>
        <node TEXT="存量 AUM 和 Bot 超限处理"/>
      </node>
      <node TEXT="权益">
        <node TEXT="AUM、Bot Limit、分润比例和周期"/>
      </node>
    </node>
    <node TEXT="HWM 分润" POSITION="left">
      <node TEXT="触发">
        <node TEXT="每笔平仓"/>
        <node TEXT="净值高于 HWM"/>
        <node TEXT="已实现盈利覆盖浮亏"/>
      </node>
      <node TEXT="不触发">
        <node TEXT="未创新高或未覆盖浮亏"/>
      </node>
      <node TEXT="计算">
        <node TEXT="可分润金额、Tier 比例、管理者所得和平台费"/>
      </node>
      <node TEXT="结算">
        <node TEXT="即时划转与周月发放"/>
        <node TEXT="幂等、冲正和重复防护"/>
      </node>
      <node TEXT="对账">
        <node TEXT="HWM、累计已实现盈亏和分润明细"/>
      </node>
    </node>
    <node TEXT="返佣" POSITION="left">
      <node TEXT="关系">
        <node TEXT="无关系、推荐关系和合伙人关系"/>
      </node>
      <node TEXT="公式">
        <node TEXT="手续费 × 用户份额占比 × 可配置比例"/>
      </node>
      <node TEXT="结算">
        <node TEXT="每日一次"/>
        <node TEXT="比例变更生效时间"/>
        <node TEXT="重复、漏发和明细对账"/>
      </node>
    </node>
    <node TEXT="控制台与全链路对账" POSITION="left">
      <node TEXT="汇总">
        <node TEXT="已发放、预计分润、待赎回和等待时长"/>
      </node>
      <node TEXT="机器人列表">
        <node TEXT="AUM、分润、待赎回、搜索和排序"/>
      </node>
      <node TEXT="用户列表">
        <node TEXT="脱敏标识、订阅金额、盈亏和订阅时间"/>
      </node>
      <node TEXT="账本守恒">
        <node TEXT="资金账户与合约账户"/>
        <node TEXT="总份额与用户权益"/>
        <node TEXT="分润账户与返佣账户"/>
      </node>
    </node>
    <node TEXT="安全与非功能" POSITION="left">
      <node TEXT="敏感数据">
        <node TEXT="UID 和邮箱脱敏"/>
        <node TEXT="API 密钥不落日志"/>
        <node TEXT="密码不回显"/>
      </node>
      <node TEXT="幂等">
        <node TEXT="订阅、赎回、分润和返佣任务"/>
      </node>
      <node TEXT="性能">
        <node TEXT="大量机器人、用户和批次峰值"/>
      </node>
      <node TEXT="可观测性">
        <node TEXT="审计日志、任务告警和资金对账告警"/>
        <node TEXT="通知失败重试"/>
      </node>
    </node>
  </node>
</map>
