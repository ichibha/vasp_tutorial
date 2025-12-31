for directory in RAMAN-*.*; do
    # ディレクトリでなければスキップ
    [ -d "$directory" ] || continue

	# ディレクトリに移動
    cd "$directory" 

    # 計算が完了していたら何もしない
	if [ -f OUTCAR ] && grep -q "EDIFF is reached" OUTCAR; then
		echo "$directory: already converged."
		cd - # 直前にいたディレクトリに移動する / 移動先を画面出力する
		continue
	fi

	# VASPを実行する
	submit_vasp

	# 直前にいたディレクトリに移動する / 移動先を画面出力する
	cd -
done

