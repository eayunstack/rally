=====
Rally
=====


什么是 Rally
=============

Rally 是 OpenStack 的一个基准测试即服务的项目。

Rally 的目的在于向社区提供一个能够在真实的部署环境上执行 **特定的** 、 **复杂的** 且 **可重复的** 测试用例的基准测试工具。

如果您看到了篇文章，想必您对 OpenStack 应该很熟悉，并且知道它是一个相当庞大的各种服务相互协作的生态系统。当出现了失败、性能低下或不能够进行扩展时，是很难对所发生的各种问题回答“发生了什么“、”为什么发生了这个问题“以及”在哪里发生了问题“的。另一个您会看到这里的原因可能是您想要构建一个 OpenStack CI/CD 系统，让您能够持续增强 OpenStack 的 SLA、性能和稳定性。

OpenStack 的 QA 团队大多在为 CI/CD 系统工作着，为了确保新的 patches 不会破坏 OpenStack 的某个单个节点的安装。从另一方面，需要清楚，这样的 CI/CD 仅仅是一个指示，而不覆盖所有的用例(例如，如果云环境在单个节点的安装中工作正常，这并不意味着它在 1 千台服务器的安装环境中也同样工作正常)。Rally 的目标是修复这些问题并帮助我们回答 ”OpenStack 如何大规模运作？“ 这样的问题。为了使其成为可能，我们将自动化并统一所有 OpenStack 大规模下的基准测试所需要的步骤：多节点 OS 的部署、验证、基准测试和分析。

**Rally** 的工作流程如下图所示：

.. image:: doc/source/images/Rally-Actions.png
   :alt: Rally Architecture


文档
=============

`Rally 文档放在 ReadTheDocs <http://rally.readthedocs.org/en/latest/> 上`_ ，是一个学习 Rally 相关内容的非常不错的文档。它提供了该基准测试工具的一个 **简单** 且具有 **解说性** 的指南。例如，请阅读 `Rally step-by-step tutorial <http://rally.readthedocs.org/en/latest/tutorial.html>`_ ，其中的很多小节，说明了如何探讨 Rally 在测试 OpenStack clouds 中的强大力量。


架构
------------

架构方面，Rally 由 4 个组要组件构成：

1. **Server Providers** - 提供服务器 (虚拟服务器)，用 ssh 访问，在一个 L3 网络中。
2. **Deploy Engines** - 在由 **Server Providers** 提供的服务器上部署 OpenStack 云。
3. **Verification** - 针对一个部署好的云环境运行 tempest (或其他特定测试) 的组件，收集结果并以人们能够解读的方式展现出来。
4. **Benchmark engine** - 可以写一些参数化的标准测试场景并在云环境上运行。


使用案例
---------

这里有 3 个高级别的 Rally 使用案例：

.. image:: doc/source/images/Rally-UseCases.png
   :alt: Rally Use Cases


Rally 致力于提供帮助的典型案例为：

- 自动化测量 & 分析，致力于新的代码修改后对 OS 性能有怎样的影响；
- 使用 Rally 分析器来监测扩展 & 性能的问题；
- 研究不同部署对 OS 性能的影响：
        - 找到一套合适的 OpenStack 部署架构；
        - 为不同的负载(控制节点、swift 节点的数量等)的负载创建部署规范；
- 为特定的 OpenStack cloud 自动化搜索最合适的硬件；
- 实现自动化生产云规范的生成：
        - 为基础云操作决定最终负载：虚拟机启动 & 停止、块设备创建/销毁 & 各种 OpenStack API 方法；
        - 检查基础云操作，以防备不同的负载。


链接
----------------------

Rally 文档：

    http://rally.readthedocs.org/en/latest/

Rally step-by-step tutorial:

    http://rally.readthedocs.org/en/latest/tutorial.html

RoadMap:

    https://docs.google.com/a/mirantis.com/spreadsheets/d/16DXpfbqvlzMFaqaXAcJsBzzpowb_XpymaK2aFY2gA2g

Launchpad page:

    https://launchpad.net/rally

Code is hosted on git.openstack.org:

    http://git.openstack.org/cgit/openstack/rally

Code is mirrored on github:

    https://github.com/openstack/rally
