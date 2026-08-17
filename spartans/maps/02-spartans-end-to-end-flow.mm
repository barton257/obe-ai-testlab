<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="SPARTANS 端到端业务流程">
    <node TEXT="1. 登录与身份分流" POSITION="right">
      <node TEXT="进入 OneBullEx">
        <node TEXT="已登录：进入 SPARTANS"/>
        <node TEXT="未登录：邮箱和密码登录">
          <node TEXT="邮箱验证码验证"/>
          <node TEXT="验证通过后进入 SPARTANS"/>
        </node>
      </node>
      <node TEXT="选择业务身份">
        <node TEXT="订阅用户流程"/>
        <node TEXT="管理者、机构或 KOL 流程"/>
      </node>
    </node>
    <node TEXT="2. 订阅用户选策略" POSITION="right">
      <node TEXT="进入策略市集">
        <node TEXT="选择 7 天、30 天或 90 天周期"/>
        <node TEXT="按收益率、AUM、订阅人数或胜率排序"/>
        <node TEXT="按机器人或策略名称搜索"/>
      </node>
      <node TEXT="查看机器人详情">
        <node TEXT="评估收益率、净值、回撤、夏普与胜率"/>
        <node TEXT="查看策略说明、资产偏好、持仓和历史订单"/>
        <node TEXT="确认公域或私域订阅资格"/>
      </node>
      <node TEXT="决定是否订阅">
        <node TEXT="不订阅：返回策略市集"/>
        <node TEXT="订阅：进入订阅配置"/>
      </node>
    </node>
    <node TEXT="3. 提交订阅" POSITION="right">
      <node TEXT="输入 USDT 金额或选择 MAX"/>
      <node TEXT="校验可用余额、最小金额、精度和 AUM 上限"/>
      <node TEXT="阅读并同意风险披露"/>
      <node TEXT="提交订阅请求">
        <node TEXT="资金预占或扣减"/>
        <node TEXT="进入下一次每小时开放窗口"/>
      </node>
      <node TEXT="批次执行">
        <node TEXT="读取包含未实现盈亏的即时每股净值"/>
        <node TEXT="订阅份额 = 处理金额 / 即时每股净值"/>
        <node TEXT="资金汇入机器人资金账户"/>
        <node TEXT="更新用户份额、总份额、AUM 和操作记录"/>
      </node>
    </node>
    <node TEXT="4. 管理者申请" POSITION="left">
      <node TEXT="进入开放平台"/>
      <node TEXT="填写申请原因、交易风格和联系方式"/>
      <node TEXT="提交管理者申请"/>
      <node TEXT="运营审核 1 至 3 个工作日">
        <node TEXT="审核通过：进入机器人控制台"/>
        <node TEXT="审核拒绝：展示原因和原申请详情">
          <node TEXT="重新编辑并提交申请"/>
        </node>
      </node>
    </node>
    <node TEXT="5. 创建与审核机器人" POSITION="left">
      <node TEXT="创建机器人">
        <node TEXT="选择公域">
          <node TEXT="一般用户可订阅"/>
        </node>
        <node TEXT="选择私域">
          <node TEXT="配置 UID 或合伙人白名单"/>
        </node>
        <node TEXT="填写英文名称、风险标签、策略标签和策略描述"/>
      </node>
      <node TEXT="提交机器人资料审核">
        <node TEXT="拒绝：修改资料后重提"/>
        <node TEXT="通过：生成机器人账户和 API 凭证"/>
      </node>
      <node TEXT="应用管理者 Tier 权益">
        <node TEXT="AUM 上限"/>
        <node TEXT="Bot 数量上限"/>
        <node TEXT="分润比例和发放周期"/>
      </node>
    </node>
    <node TEXT="6. 聚合资金统一交易" POSITION="right">
      <node TEXT="管理者处理订阅资金">
        <node TEXT="从资金账户划转至合约账户"/>
        <node TEXT="API 划转或手动划转"/>
      </node>
      <node TEXT="执行合约交易">
        <node TEXT="API 自动交易"/>
        <node TEXT="机器人虚拟账户手动交易"/>
        <node TEXT="统一开仓、平仓、成本与风险敞口"/>
      </node>
      <node TEXT="更新资金池">
        <node TEXT="已实现盈亏"/>
        <node TEXT="未实现盈亏"/>
        <node TEXT="交易手续费与资金费"/>
        <node TEXT="账户净值和每股净值"/>
        <node TEXT="按份额映射用户权益与盈亏"/>
      </node>
    </node>
    <node TEXT="7. 我的订阅" POSITION="right">
      <node TEXT="查看总权益、资产构成和组合盈亏"/>
      <node TEXT="查看 7 天、30 天、90 天统计"/>
      <node TEXT="查看进行中机器人">
        <node TEXT="运行中资产"/>
        <node TEXT="原订阅金额"/>
        <node TEXT="盈亏与收益率"/>
      </node>
      <node TEXT="查看操作记录">
        <node TEXT="订阅和赎回"/>
        <node TEXT="金额、状态和时间"/>
      </node>
      <node TEXT="用户下一步">
        <node TEXT="继续运行"/>
        <node TEXT="追加资金：回到订阅配置"/>
        <node TEXT="发起部分或全部赎回"/>
      </node>
    </node>
    <node TEXT="8. 赎回与流动性队列" POSITION="right">
      <node TEXT="提交赎回">
        <node TEXT="查看资产金额、赎回中和可赎回"/>
        <node TEXT="输入金额或选择 MAX"/>
        <node TEXT="提示交易中金额可能波动"/>
      </node>
      <node TEXT="按处理时净值计算赎回权益"/>
      <node TEXT="机器人全部平仓">
        <node TEXT="按份额全部赎回"/>
      </node>
      <node TEXT="机器人仍有仓位">
        <node TEXT="进入每小时批次队列"/>
        <node TEXT="检查资金账户流动性">
          <node TEXT="足够：扣减资金并完成赎回"/>
          <node TEXT="不足：当前请求继续排队"/>
        </node>
        <node TEXT="继续检查后续可满足的小额请求"/>
        <node TEXT="管理者从合约账户划转资金后重试"/>
      </node>
      <node TEXT="完成赎回">
        <node TEXT="资金返回用户账户"/>
        <node TEXT="扣减用户份额和总份额"/>
        <node TEXT="更新 AUM、净值和操作记录"/>
      </node>
    </node>
    <node TEXT="9. 赎回超时介入" POSITION="left">
      <node TEXT="等待期间每小时发送邮件"/>
      <node TEXT="超过 5 天">
        <node TEXT="Lark 每日提醒运营与 BD"/>
        <node TEXT="跟进管理者补充流动性"/>
      </node>
      <node TEXT="超过 7 天">
        <node TEXT="平台强制介入"/>
        <node TEXT="无法联系管理者">
          <node TEXT="暂停机器人"/>
          <node TEXT="强平仓位"/>
          <node TEXT="自动赎回用户资金"/>
          <node TEXT="清算或下架"/>
        </node>
        <node TEXT="理由充分">
          <node TEXT="延长等待期"/>
          <node TEXT="每日追踪"/>
        </node>
      </node>
    </node>
    <node TEXT="10. 分润、返佣与评级" POSITION="left">
      <node TEXT="HWM 分润">
        <node TEXT="每笔平仓触发"/>
        <node TEXT="即时净值高于 HWM"/>
        <node TEXT="累计已实现盈利覆盖未实现亏损"/>
        <node TEXT="计算可分润金额"/>
        <node TEXT="按 Tier 拆分管理者所得与平台费"/>
        <node TEXT="按周或月发放"/>
      </node>
      <node TEXT="手续费返佣">
        <node TEXT="每笔成交判断推荐或合伙人关系"/>
        <node TEXT="手续费 × 用户份额占比 × 返佣比例"/>
        <node TEXT="每日结算"/>
      </node>
      <node TEXT="Tier 评级">
        <node TEXT="投入自有资金时即时判断"/>
        <node TEXT="每日 UTC+0 判断升级"/>
        <node TEXT="每周一分润后判断降级"/>
      </node>
    </node>
  </node>
</map>
