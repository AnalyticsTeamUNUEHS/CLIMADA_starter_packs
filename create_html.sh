#!/bin/zsh

setopt null_glob

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR="$ROOT_DIR/build/intermediate_files"
OUT_DIR="$ROOT_DIR/build"

mkdir -p "$TMP_DIR"
# rm -r "$TMP_DIR"/*

for pack_dir in "$ROOT_DIR"/starter_pack_*; do
	pack_name="$(basename "$pack_dir")"
	sources=()

	sources+=("$pack_dir/README.md")

	for nb in "$pack_dir"/notebooks/*.ipynb; do
		sources+=("$nb")
	done

	idx=1
	for src in "${sources[@]}"; do
		seq=$(printf "%03d" "$idx")
		ext="${src##*.}"
		src_name="$(basename "${src%.*}")"

		out_md="$TMP_DIR/${seq}_${pack_name}_${src_name}.md"

		if [[ -f "$out_md" ]]; then
			echo "File exists already: $out_md"
			idx=$((idx + 1))
			continue
		fi

		echo "Creating file $out_md"
		if [[ "$ext" == "md" ]]; then
			pandoc "$src" -t gfm -o "$out_md"
		elif [[ "$ext" == "ipynb" ]]; then
			jupyter nbconvert --to markdown "$src" --output "${out_md:t:r}" --output-dir "$TMP_DIR"
		fi

		idx=$((idx + 1))
	done

	md_parts=("$TMP_DIR"/[0-9][0-9][0-9]_${pack_name}_*.md)

	out_html="$pack_dir/${pack_name}.html"

	pandoc "${md_parts[@]}" \
		--standalone \
		--toc \
		--toc-depth=2 \
		--number-sections \
		--css "$ROOT_DIR/build/pandoc.css" \
		--metadata title="$pack_name" \
		--resource-path "$TMP_DIR:$pack_dir" \
		--embed-resources \
		-o "$out_html"

	echo "Created $out_html"
done
