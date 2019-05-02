# FastlaneExample

fastlane 包含一组 Ruby 实现的工具集,能完成 iOS 和 Android 工程 的自动化构建\测试和发布等功能。网上入门的解说很多，中文可以参照这个：https://github.com/mythkiven/AD_Fastlane 官方文档：https://docs.fastlane.tools/ 个人安装过程中，遇到的ruby问题较多，可以先了解下ruby的几个概念：https://henter.me/post/ruby-rvm-gem-rake-bundle-rails.html。

demo结合makefile，实现了fastlane + bugly, fastlane + itunesConnect的一键操作。

上传itunesConnect时，可使用csvToJson.py, fastconfig.py这两个脚本直接将运营小妹的更新文件（.xlsx）转换成fastlane使用的Deliverfile,进一步完善
一键操作的初衷。
