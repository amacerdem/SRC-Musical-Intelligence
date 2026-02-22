import { useEffect, useState } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import { fetchJSON } from '../api/client';
import { colors } from '../design/tokens';

interface DocNode {
  name: string;
  type: 'file' | 'directory';
  path: string;
  children?: DocNode[];
}

interface DocContent {
  content: string;
  path: string;
}

function TreeItem({ node, depth, onSelect, selected }: {
  node: DocNode;
  depth: number;
  onSelect: (path: string) => void;
  selected: string | null;
}) {
  const [expanded, setExpanded] = useState(depth < 2);
  const isDir = node.type === 'directory';
  const isSelected = selected === node.path;
  const hasChildren = isDir && node.children && node.children.length > 0;

  // Check if directory has content (non-empty)
  const isEmpty = isDir && (!node.children || node.children.length === 0);

  return (
    <div>
      <div
        className="flex items-center gap-1.5 py-1 px-2 rounded-lg cursor-pointer transition-colors text-sm"
        style={{
          paddingLeft: depth * 16 + 8,
          background: isSelected ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
          color: isEmpty ? 'var(--text-muted)' : isDir ? 'var(--text-secondary)' : 'var(--text-primary)',
        }}
        onClick={() => {
          if (isDir) setExpanded(!expanded);
          else onSelect(node.path);
        }}
      >
        <span className="text-xs w-4 text-center">
          {isDir ? (expanded ? '▾' : '▸') : ''}
        </span>
        <span className="truncate">{node.name}</span>
        {isEmpty && <span className="text-xs ml-auto" style={{ color: 'var(--text-muted)' }}>○</span>}
      </div>
      {expanded && hasChildren && node.children!.map((child) => (
        <TreeItem
          key={child.path}
          node={child}
          depth={depth + 1}
          onSelect={onSelect}
          selected={selected}
        />
      ))}
    </div>
  );
}

export default function Documentation() {
  const [tree, setTree] = useState<DocNode | null>(null);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [content, setContent] = useState<string>('');
  const [loadingTree, setLoadingTree] = useState(true);

  useEffect(() => {
    fetchJSON<DocNode>('/docs/tree')
      .then(setTree)
      .catch(console.error)
      .finally(() => setLoadingTree(false));
  }, []);

  const loadDoc = async (path: string) => {
    setSelectedPath(path);
    try {
      const doc = await fetchJSON<DocContent>(`/docs/content?path=${encodeURIComponent(path)}`);
      setContent(doc.content);
    } catch (e) {
      setContent(`Error loading document: ${e}`);
    }
  };

  return (
    <div className="flex gap-4 p-4 h-full overflow-hidden">
      {/* Tree sidebar */}
      <GlassPanel className="p-3 overflow-y-auto" style={{ width: 300, minWidth: 250 }}>
        <h3 className="text-sm font-medium px-2 py-2 mb-1" style={{ color: 'var(--text-secondary)' }}>
          C³-Brain · F1–F12
        </h3>
        {loadingTree ? (
          <div className="text-xs px-2" style={{ color: 'var(--text-muted)' }}>Loading...</div>
        ) : tree ? (
          tree.children?.map((child) => (
            <TreeItem key={child.path} node={child} depth={0} onSelect={loadDoc} selected={selectedPath} />
          ))
        ) : (
          <div className="text-xs px-2" style={{ color: 'var(--text-muted)' }}>No docs found</div>
        )}
      </GlassPanel>

      {/* Content viewer */}
      <GlassPanel className="flex-1 p-6 overflow-y-auto">
        {content ? (
          <div
            className="prose prose-invert prose-sm max-w-none"
            style={{
              color: 'var(--text-primary)',
              fontFamily: 'Inter, sans-serif',
              lineHeight: 1.7,
            }}
          >
            <pre className="whitespace-pre-wrap text-sm font-data" style={{
              background: 'rgba(255,255,255,0.03)',
              padding: 16,
              borderRadius: 12,
              border: '1px solid rgba(255,255,255,0.06)',
              color: 'var(--text-primary)',
            }}>
              {content}
            </pre>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
              Select a document from the tree
            </p>
          </div>
        )}
      </GlassPanel>
    </div>
  );
}
