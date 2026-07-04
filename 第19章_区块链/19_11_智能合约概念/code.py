#!/usr/bin/env python3
"""真实执行源码 — 19_11_智能合约概念"""
def exp_19_11():
    """实验11: 智能合约概念"""
    eid = '19_11_智能合约概念'
    d = exp_start(eid, '智能合约概念')
    files = []

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    sc = (
        '                    智能合约 (Smart Contract)\n'
        '  ┌────────────────────────────────────────────────────┐\n'
        '  │                                                     │\n'
        '  │  contract SimpleAuction {                          │\n'
        '  │      address public beneficiary;                   │\n'
        '  │      uint public auctionEndTime;                   │\n'
        '  │                                                     │\n'
        '  │      function bid() public payable {               │\n'
        '  │          require(now <= auctionEndTime);            │\n'
        '  │          // 自动执行出价逻辑                         │\n'
        '  │          if (highestBid > 0) {                      │\n'
        '  │              pendingReturns[msg.sender] += bid;    │\n'
        '  │          }                                          │\n'
        '  │      }                                              │\n'
        '  │  }                                                  │\n'
        '  │                                                     │\n'
        '  │  特点:                                              │\n'
        '  │  • 自动执行 (代码即法律)                             │\n'
        '  │  • 不可篡改 (部署后无法修改)                         │\n'
        '  │  • 透明可审计 (所有人可见)                           │\n'
        '  │  • 去中心化 (无中间人)                               │\n'
        '  │  • 可组合 (乐高式拼接)                               │\n'
        '  └────────────────────────────────────────────────────┘'
    )
    ax.text(0.5, 0.5, sc, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#E8F5E9'))
    ax.set_title('智能合约原理 (Solidity示例)', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_智能合约.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
