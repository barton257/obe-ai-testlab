<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="SPARTANS 业务全景">
    <node TEXT="产品定位" POSITION="right">
      <node TEXT="To B：策略管理与配资平台">
        <node TEXT="管理者投入自有资金"/>
        <node TEXT="Tier 决定 AUM、Bot 数量与分润额度"/>
        <node TEXT="手动或 API 统一执行合约交易"/>
      </node>
      <node TEXT="To C：优质策略公开与私域市场">
        <node TEXT="用户选择机器人"/>
        <node TEXT="订阅获得资金池份额 Share"/>
        <node TEXT="按份额承担收益、亏损与费用"/>
      </node>
      <node TEXT="核心价值">
        <node TEXT="统一资金池与统一成交成本"/>
        <node TEXT="减少滑点、延迟、漏单和成交价差异"/>
        <node TEXT="保持策略执行一致性与完整性"/>
        <node TEXT="支持规模化策略和专业资产管理"/>
      </node>
    </node>
    <node TEXT="业务角色" POSITION="right">
      <node TEXT="订阅用户">
        <node TEXT="浏览与评估策略"/>
        <node TEXT="订阅和追加资金"/>
        <node TEXT="查看权益、绩效与操作记录"/>
        <node TEXT="发起部分或全部赎回"/>
      </node>
      <node TEXT="机器人管理者">
        <node TEXT="量化交易机构"/>
        <node TEXT="手操交易者"/>
        <node TEXT="KOL 与合作伙伴"/>
        <node TEXT="管理资金、仓位与风险敞口"/>
        <node TEXT="为赎回提供资金账户流动性"/>
      </node>
      <node TEXT="平台运营">
        <node TEXT="审核管理者资格"/>
        <node TEXT="审核机器人资料"/>
        <node TEXT="维护 Tier 与运营参数"/>
        <node TEXT="处理赎回超时"/>
        <node TEXT="暂停、清算或下架机器人"/>
      </node>
      <node TEXT="BD、推荐人与合伙人">
        <node TEXT="维护私域用户关系"/>
        <node TEXT="推荐和合伙人关系"/>
        <node TEXT="获得手续费返佣"/>
      </node>
    </node>
    <node TEXT="策略市场" POSITION="right">
      <node TEXT="公域机器人">
        <node TEXT="一般用户可订阅"/>
        <node TEXT="满足公开条件后进入市集"/>
      </node>
      <node TEXT="私域机器人">
        <node TEXT="UID 白名单"/>
        <node TEXT="合伙人关系白名单"/>
      </node>
      <node TEXT="市集列表">
        <node TEXT="默认每页 12 个"/>
        <node TEXT="7 天、30 天、90 天周期"/>
        <node TEXT="按收益率、资产规模、订阅人数、胜率排序"/>
        <node TEXT="按机器人或策略名称搜索"/>
      </node>
      <node TEXT="机器人详情">
        <node TEXT="收益率、单位净值和最大回撤"/>
        <node TEXT="夏普、胜率和交易统计"/>
        <node TEXT="资产偏好、当前持仓和历史订单"/>
        <node TEXT="分润比例、状态和策略说明"/>
      </node>
    </node>
    <node TEXT="统一资金池" POSITION="left">
      <node TEXT="份额与净值">
        <node TEXT="每股净值 = 机器人账户总资产 / 总份额"/>
        <node TEXT="用户权益 = 用户份额 × 当前每股净值"/>
      </node>
      <node TEXT="订阅">
        <node TEXT="每小时批次处理"/>
        <node TEXT="按处理时净值铸造份额"/>
        <node TEXT="订阅资金进入机器人资金账户"/>
      </node>
      <node TEXT="交易">
        <node TEXT="资金账户划转至合约账户"/>
        <node TEXT="聚合资金统一开仓和平仓"/>
        <node TEXT="已实现盈亏、浮盈亏、手续费和资金费进入净值"/>
      </node>
      <node TEXT="赎回">
        <node TEXT="按处理时每股净值计算"/>
        <node TEXT="全部平仓时可按份额全部赎回"/>
        <node TEXT="每小时批次检查资金账户流动性"/>
        <node TEXT="资金不足则进入赎回队列"/>
        <node TEXT="管理者从合约账户划转至资金账户"/>
      </node>
      <node TEXT="关键账务口径">
        <node TEXT="订阅总额"/>
        <node TEXT="资金账户余额"/>
        <node TEXT="合约账户权益"/>
        <node TEXT="管理资产规模 AUM"/>
        <node TEXT="用户运行中资产"/>
      </node>
    </node>
    <node TEXT="管理者生命周期" POSITION="left">
      <node TEXT="申请开放平台">
        <node TEXT="申请原因与交易风格"/>
        <node TEXT="联系方式"/>
      </node>
      <node TEXT="资格审核">
        <node TEXT="未申请"/>
        <node TEXT="审核中"/>
        <node TEXT="审核通过"/>
        <node TEXT="审核拒绝与重新申请"/>
      </node>
      <node TEXT="创建机器人">
        <node TEXT="选择公域或私域"/>
        <node TEXT="英文名称且不允许空格"/>
        <node TEXT="风险与策略类型标签"/>
        <node TEXT="策略描述"/>
      </node>
      <node TEXT="机器人资料审核">
        <node TEXT="待审核"/>
        <node TEXT="通过后生成机器人账户和 API 凭证"/>
        <node TEXT="运行中、暂停、清算或下架"/>
      </node>
      <node TEXT="控制台能力">
        <node TEXT="数据"/>
        <node TEXT="账户"/>
        <node TEXT="API"/>
        <node TEXT="机器人信息"/>
        <node TEXT="订阅用户与私域白名单"/>
      </node>
    </node>
    <node TEXT="Tier 等级" POSITION="left">
      <node TEXT="评级条件">
        <node TEXT="管理者自有资金"/>
        <node TEXT="30 日 ROI"/>
        <node TEXT="30 日最大回撤 MDD"/>
        <node TEXT="30 日平均赎回时效"/>
        <node TEXT="30 日交易量"/>
        <node TEXT="无违规硬性条件"/>
      </node>
      <node TEXT="等级权益">
        <node TEXT="AUM 上限"/>
        <node TEXT="Bot 数量上限"/>
        <node TEXT="Profit Sharing 比例"/>
        <node TEXT="周分润或月分润"/>
        <node TEXT="Tier 5 专人产研支持"/>
      </node>
      <node TEXT="评定节奏">
        <node TEXT="投入自有资金时即时判断"/>
        <node TEXT="每日 UTC+0 判断升级"/>
        <node TEXT="每周一分润结束后判断降级"/>
      </node>
    </node>
    <node TEXT="收益体系" POSITION="left">
      <node TEXT="HWM 分润">
        <node TEXT="每笔平仓触发判断"/>
        <node TEXT="即时净值高于历史高水位"/>
        <node TEXT="累计已实现盈利覆盖未实现亏损"/>
        <node TEXT="可分润金额 × Tier 分润比例"/>
        <node TEXT="管理者所得与平台使用费拆分"/>
      </node>
      <node TEXT="手续费返佣">
        <node TEXT="机器人账户每笔成交触发归属计算"/>
        <node TEXT="按用户份额占比分摊手续费"/>
        <node TEXT="推荐或合伙人关系"/>
        <node TEXT="返佣比例可配置"/>
        <node TEXT="每日结算"/>
      </node>
      <node TEXT="其他收益">
        <node TEXT="订阅费分成尚未启用"/>
        <node TEXT="斯巴达竞技场活动奖励"/>
      </node>
    </node>
    <node TEXT="风险与运营" POSITION="left">
      <node TEXT="用户风险">
        <node TEXT="订阅前确认风险披露"/>
        <node TEXT="合约交易和净值波动"/>
        <node TEXT="历史收益不保证未来盈利"/>
      </node>
      <node TEXT="赎回流动性">
        <node TEXT="每小时发送队列等待邮件"/>
        <node TEXT="超过 5 天通知运营与 BD"/>
        <node TEXT="超过 7 天平台强制介入"/>
      </node>
      <node TEXT="强制处置">
        <node TEXT="暂停机器人"/>
        <node TEXT="强平仓位并自动赎回"/>
        <node TEXT="清算或下架"/>
        <node TEXT="有充分理由时延期并每日追踪"/>
      </node>
      <node TEXT="敏感凭证">
        <node TEXT="机器人虚拟账号与密码"/>
        <node TEXT="身份验证器"/>
        <node TEXT="API Key 与 Secret Key"/>
      </node>
      <node TEXT="全链路对账">
        <node TEXT="总份额与每股净值"/>
        <node TEXT="AUM 与用户权益"/>
        <node TEXT="分润与返佣"/>
        <node TEXT="订阅和赎回操作记录"/>
      </node>
    </node>
  </node>
</map>
